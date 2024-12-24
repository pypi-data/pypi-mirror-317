import pandas as pd

class NetworkDiagram:
    def __init__(self, df):
        """
        Initializes the NetworkDiagram with the provided DataFrame.

        Parameters:
        df (pd.DataFrame): DataFrame containing project activities and durations.
                           Expected columns: 'Activity', 'Duration',
                                            'Activity.1', 'Duration.1',
                                            'Activity.2', 'Duration.2',
                                            'Activity.3', 'Duration.3'
        """
        self.df = df.copy()
        self.start = None
        self.PDN = None
        self.PCT = None
        self.one_lop = None
        self.two_lop = None
        self.three_lop = None
        self.IMP = None
        self.finish = None

        # Perform calculations
        self._calculate_network()

    def _calculate_network(self):
        """Performs the CPM calculations and stores results in class attributes."""
        self._initialize_start()
        self._process_PDN()
        self._process_PCT()
        self._process_LOP()
        self._process_IMP()
        self._initialize_finish()
        self._calculate_finish_values()
        self._backward_pass()

    def _initialize_start(self):
        """Initializes the Start activity DataFrame."""
        start = {
            'Activity_S': ['Start'],
            'ES_S': [0],
            'Duration_S': [0]
        }
        self.start = pd.DataFrame(start)
        self.start['EF_S'] = self.start['ES_S'] + self.start['Duration_S']

    def _process_PDN(self):
        """Processes PDN activities."""
        PDN = self.df[['Activity', 'Duration']].copy()
        PDN['ES'] = int(self.start['EF_S'].iloc[0])
        PDN['EF'] = PDN['Duration'] + PDN['ES']
        self.PDN = PDN

    def _process_PCT(self):
        """Processes PCT activities."""
        PCT = self.df[['Activity.1', 'Duration.1']].copy()
        PCT['ES.1'] = int(self.PDN['EF'].max())
        PCT['EF.1'] = PCT['Duration.1'] + PCT['ES.1']
        self.PCT = PCT

    def _process_LOP(self):
        """Processes Levels of Precedence (LOP) activities."""
        # Process LOP_1
        LOP_1 = self.df[['Activity.2', 'Duration.2']].dropna().copy()

        # Process one_lop
        if len(LOP_1) >= 1:
            one_lop = pd.DataFrame(LOP_1.iloc[0]).T
            one_lop.rename(columns={'Activity.2': 'Activity.2.1','Duration.2': 'Duration.2.1'}, inplace=True)
            one_lop['ES.2.1'] = int(self.PCT['EF.1'].max())
            one_lop['EF.2.1'] = one_lop['Duration.2.1'] + one_lop['ES.2.1']
            self.one_lop = one_lop
        else:
            self.one_lop = pd.DataFrame()

        # Process two_lop
        if len(LOP_1) >= 2:
            two_lop = pd.DataFrame(LOP_1.iloc[1]).T
            two_lop.rename(columns={'Activity.2': 'Activity.2.2', 'Duration.2': 'Duration.2.2'}, inplace=True)
            two_lop['ES.2.2'] = int(self.one_lop['EF.2.1'].iloc[0]) if not self.one_lop.empty else int(self.PCT['EF.1'].max())
            two_lop['EF.2.2'] = two_lop['Duration.2.2'] + two_lop['ES.2.2']
            self.two_lop = two_lop
        else:
            self.two_lop = pd.DataFrame()

        # Process three_lop
        if len(LOP_1) >= 3:
            three_lop = pd.DataFrame(LOP_1.iloc[2]).T
            three_lop.rename(columns={'Activity.2': 'Activity.2.3', 'Duration.2': 'Duration.2.3'}, inplace=True)
            three_lop['ES.2.3'] = int(self.two_lop['EF.2.2'].iloc[0]) if not self.two_lop.empty else int(self.one_lop['EF.2.1'].iloc[0]) if not self.one_lop.empty else int(self.PCT['EF.1'].max())
            three_lop['EF.2.3'] = three_lop['Duration.2.3'] + three_lop['ES.2.3']
            self.three_lop = three_lop
        else:
            self.three_lop = pd.DataFrame()

    def _process_IMP(self):
        """Processes IMP activities."""
        IMP = self.df[['Activity.3', 'Duration.3']].copy()
        if not self.three_lop.empty:
            imp_es = int(self.three_lop['EF.2.3'].iloc[0])
        elif not self.two_lop.empty:
            imp_es = int(self.two_lop['EF.2.2'].iloc[0])
        elif not self.one_lop.empty:
            imp_es = int(self.one_lop['EF.2.1'].iloc[0])
        else:
            imp_es = int(self.PCT['EF.1'].max())
        IMP['ES.3'] = imp_es
        IMP['EF.3'] = IMP['Duration.3'] + IMP['ES.3']
        self.IMP = IMP

    def _initialize_finish(self):
        """Initializes the Finish activity DataFrame."""
        finish = {
            'Activity_F': ['Finish'],
            'ES_F': int(self.IMP['EF.3'].max()) if not self.IMP.empty else 0,
            'Duration_F': [0]
        }
        self.finish = pd.DataFrame(finish)
        self.finish['EF_F'] = self.finish['ES_F'] + self.finish['Duration_F']

    def _calculate_finish_values(self):
        """Calculates LF, LS, and Slack for Finish and IMP."""
        # Finish calculations
        self.finish['LF_F'] = self.finish['EF_F']
        self.finish['Slack_F'] = self.finish['LF_F'] - self.finish['EF_F']
        self.finish['LS_F'] = self.finish['LF_F'] - self.finish['Duration_F']

        # IMP calculations
        if not self.IMP.empty:
            self.IMP['LF.3'] = int(self.finish['LS_F'].iloc[0])
            self.IMP['Slack.3'] = self.IMP['LF.3'] - self.IMP['EF.3']
            self.IMP['LS.3'] = self.IMP['LF.3'] - self.IMP['Duration.3']

    def _backward_pass(self):
        """Performs backward pass to calculate LF, LS, and Slack for all activities."""
        # Calculate for three_lop
        if not self.three_lop.empty:
            self.three_lop['LF.2.3'] = int(self.IMP['LS.3'].min())
            self.three_lop['Slack.2.3'] = self.three_lop['LF.2.3'] - self.three_lop['EF.2.3']
            self.three_lop['LS.2.3'] = self.three_lop['LF.2.3'] - self.three_lop['Duration.2.3']

        # Calculate for two_lop
        if not self.two_lop.empty:
            lf_2_2 = int(self.three_lop['LS.2.3'].iloc[0]) if not self.three_lop.empty else int(self.IMP['LS.3'].min())
            self.two_lop['LF.2.2'] = lf_2_2
            self.two_lop['Slack.2.2'] = self.two_lop['LF.2.2'] - self.two_lop['EF.2.2']
            self.two_lop['LS.2.2'] = self.two_lop['LF.2.2'] - self.two_lop['Duration.2.2']

        # Calculate for one_lop
        if not self.one_lop.empty:
            lf_2_1 = int(self.two_lop['LS.2.2'].iloc[0]) if not self.two_lop.empty else int(self.three_lop['LS.2.3'].iloc[0]) if not self.three_lop.empty else int(self.IMP['LS.3'].min())
            self.one_lop['LF.2.1'] = lf_2_1
            self.one_lop['Slack.2.1'] = self.one_lop['LF.2.1'] - self.one_lop['EF.2.1']
            self.one_lop['LS.2.1'] = self.one_lop['LF.2.1'] - self.one_lop['Duration.2.1']

        # Calculate for PCT
        if not self.PCT.empty:
            lf_1 = int(self.one_lop['LS.2.1'].min()) if not self.one_lop.empty else int(self.two_lop['LS.2.2'].min()) if not self.two_lop.empty else int(self.three_lop['LS.2.3'].min()) if not self.three_lop.empty else int(self.IMP['LS.3'].min())
            self.PCT['LF.1'] = lf_1
            self.PCT['Slack.1'] = self.PCT['LF.1'] - self.PCT['EF.1']
            self.PCT['LS.1'] = self.PCT['LF.1'] - self.PCT['Duration.1']
            self.PCT.dropna(inplace=True)

        # Calculate for PDN
        if not self.PDN.empty:
            lf_pdn = int(self.PCT['LS.1'].min()) if not self.PCT.empty else int(self.one_lop['LS.2.1'].min()) if not self.one_lop.empty else int(self.IMP['LS.3'].min())
            self.PDN['LF'] = lf_pdn
            self.PDN['Slack'] = self.PDN['LF'] - self.PDN['EF']
            self.PDN['LS'] = self.PDN['LF'] - self.PDN['Duration']
            self.PDN.dropna(inplace=True)

        # Calculate for Start
        if not self.start.empty and not self.PDN.empty:
            lf_start = int(self.PDN['LS'].min())
            self.start['LF_S'] = lf_start
            self.start['Slack_S'] = self.start['LF_S'] - self.start['EF_S']
            self.start['LS_S'] = self.start['LF_S'] - self.start['Duration_S']
            self.start.dropna(inplace=True)

    def get_network_diagram(self):
        """Returns the complete network diagram by concatenating all DataFrames."""
        dfs = [self.start, self.PDN, self.PCT, self.one_lop, self.two_lop, self.three_lop, self.IMP, self.finish]
        network_diagram = pd.concat(dfs, axis=1)
        return network_diagram

    def get_critical_path(self):
        """Extracts and returns the critical path activities (Slack == 0)."""
        critical_path = pd.DataFrame()

        # Check and concatenate activities with zero slack
        if not self.PDN.empty:
            cp_pdn = self.PDN[self.PDN['Slack'] == 0]
            critical_path = pd.concat([critical_path, cp_pdn], ignore_index=True)

        if not self.PCT.empty:
            cp_pct = self.PCT[self.PCT['Slack.1'] == 0]
            critical_path = pd.concat([critical_path, cp_pct], ignore_index=True)

        if not self.one_lop.empty:
            cp_one_lop = self.one_lop[self.one_lop['Slack.2.1'] == 0]
            critical_path = pd.concat([critical_path, cp_one_lop], ignore_index=True)

        if not self.two_lop.empty:
            cp_two_lop = self.two_lop[self.two_lop['Slack.2.2'] == 0]
            critical_path = pd.concat([critical_path, cp_two_lop], ignore_index=True)

        if not self.three_lop.empty:
            cp_three_lop = self.three_lop[self.three_lop['Slack.2.3'] == 0]
            critical_path = pd.concat([critical_path, cp_three_lop], ignore_index=True)

        if not self.IMP.empty:
            cp_imp = self.IMP[self.IMP['Slack.3'] == 0]
            critical_path = pd.concat([critical_path, cp_imp], ignore_index=True)

        if not self.start.empty:
            cp_start = self.start[self.start['Slack_S'] == 0]
            critical_path = pd.concat([critical_path, cp_start], ignore_index=True)

        if not self.finish.empty:
            cp_finish = self.finish[self.finish['Slack_F'] == 0]
            critical_path = pd.concat([critical_path, cp_finish], ignore_index=True)

        return critical_path.reset_index(drop=True)


class NetworkDiagramExporter:
    def __init__(self, network_diagram=None, filename="network_diagram.xlsx"):
        """
        Initializes the exporter with a NetworkDiagram instance and an output filename.
        
        Parameters:
        network_diagram: An instance of NetworkDiagram with computed attributes:
                         start, PDN, PCT, one_lop, two_lop, three_lop, IMP, finish
        filename (str): The name of the Excel file to be created.
        """
        self.nd = network_diagram
        self.filename = filename

        # Store each section in a list. Each is a tuple: (dataframe, label)
        self.sections = [
            (self.nd.start, "Start"),
            (self.nd.PDN, "PDN"),
            (self.nd.PCT, "PCT"),
            (self.nd.one_lop, "LOP1"),
            (self.nd.two_lop, "LOP2"),
            (self.nd.three_lop, "LOP3"),
            (self.nd.IMP, "IMP"),
            (self.nd.finish, "Finish")
        ]

    def export(self):
        """
        Exports the network diagram into an Excel file with formatting.
        """
        if self.nd is None:
            raise ValueError("No network_diagram provided to the exporter.")

        with pd.ExcelWriter(self.filename, engine='xlsxwriter') as writer:
            workbook = writer.book
            worksheet = workbook.add_worksheet("NetworkDiagram")
            
            # Define cell formats
            style_format = workbook.add_format({'bg_color': '#ff6929', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
            white_format = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'})
            activity_format = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'bold': True})

            # Set a uniform column width for clarity
            worksheet.set_column(0, 100, 12)

            # Define spacing parameters
            base_col = 1          # Start from column B (0-based indexing)
            section_gap = 3       # Number of blank columns between sections
            block_width = 3       # Each block is 3 columns wide

            # Current column to place the first section
            current_col = base_col

            # Write all sections
            for df, label in self.sections:
                if df is not None and not df.empty:
                    # Write this section starting at current_col
                    self._write_section(worksheet, df, label, current_col, style_format, white_format, activity_format)

                    # Move current_col to the next section, leaving a gap of 3 columns
                    current_col = current_col + block_width + section_gap

            # The file is written automatically at the end of the 'with' block.

    def _write_section(self, worksheet, df, label, start_col, style_format, white_format, activity_format):
        """
        Writes a single section (one of the sets of activities) onto the worksheet.
        
        Each activity block is a 3x3 grid:
        Top row: ES | Slack | EF
        Middle row: Activity Name (merged across 3 cells)
        Bottom row: LS | Duration | LF

        One blank row is left between subsequent activity blocks of the same section.
        """
        # Start row for each section category
        # You can adjust if you want to start lower, but for now, row = 1
        row = 1

        # Identify column names based on patterns:
        es_col = [c for c in df.columns if c.startswith('ES')][0]
        ef_col = [c for c in df.columns if c.startswith('EF')][0]
        ls_col = [c for c in df.columns if c.startswith('LS')][0]
        lf_col = [c for c in df.columns if c.startswith('LF')][0]
        slack_col = [c for c in df.columns if c.startswith('Slack')][0]
        dur_col = [c for c in df.columns if c.startswith('Duration')][0]
        act_col = [c for c in df.columns if c.startswith('Activity')][0]

        # Iterate through each activity in the DataFrame
        for i in range(len(df)):
            activity = df.iloc[i]

            ES = activity[es_col]
            EF = activity[ef_col]
            LS = activity[ls_col]
            LF = activity[lf_col]
            Slack = activity[slack_col]
            Duration = activity[dur_col]
            ActName = activity[act_col]

            # Determine if this block should be green or white
            cell_format = style_format if Slack == 0 else white_format
            act_format = style_format if Slack == 0 else activity_format

            # Write the top row: ES | Slack | EF
            worksheet.write(row,     start_col,     ES,    cell_format)
            worksheet.write(row,     start_col + 1, Slack, cell_format)
            worksheet.write(row,     start_col + 2, EF,    cell_format)

            # Middle row: Activity name (spread across 3 cells)
            worksheet.merge_range(row+1, start_col, row+1, start_col+2, ActName, act_format)

            # Bottom row: LS | Duration | LF
            worksheet.write(row+2, start_col,     LS,       cell_format)
            worksheet.write(row+2, start_col + 1, Duration, cell_format)
            worksheet.write(row+2, start_col + 2, LF,       cell_format)

            # Move down for the next activity block of the same section
            # 3 rows for the block + 1 blank row = 4 rows total
            row += 4
