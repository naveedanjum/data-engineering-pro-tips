import pandas as pd


class DataUtils:
    """
    Utility class for efficient data processing in Python.
    """

    @staticmethod
    def read_large_file(file_path, chunk_size=100000):
        """
        Reads a large file line by line using a generator.
        :param file_path: Path to the file.
        :param chunk_size: Number of rows per chunk.
        :return: Generator yielding data chunks.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                yield line.strip()

    @staticmethod
    def optimize_dataframe(df):
        """
        Optimizes DataFrame memory usage by converting data types where applicable.
        """
        before_memory = df.memory_usage().sum()

        for col in df.select_dtypes(include=['int64', 'int32']).columns:
            df[col] = pd.to_numeric(df[col], downcast='integer')

        for col in df.select_dtypes(include=['float64', 'float32']).columns:
            df[col] = pd.to_numeric(df[col], downcast='float')

        for col in df.select_dtypes(include=['object']).columns:
            num_unique_values = len(df[col].unique())
            num_total_values = len(df[col])
            if num_unique_values / num_total_values < 0.5:
                df[col] = df[col].astype('category')

        after_memory = df.memory_usage().sum()

        print(f"✅ Memory usage reduced from {before_memory / (1024)} KB to {after_memory / (1024)} KB")
        return df

    @staticmethod
    def convert_csv_to_parquet(csv_path, parquet_path):
        """
        Converts a CSV file to Parquet format for optimized storage.
        :param csv_path: Path to CSV file.
        :param parquet_path: Path to save Parquet file.
        """
        df = pd.read_csv(csv_path)
        df = DataUtils.optimize_dataframe(df)
        df.to_parquet(parquet_path, engine="pyarrow", compression="snappy")

    @staticmethod
    def chain_transformations(df):
        """
        Performs method chaining for optimized data transformation.
        :param df: Pandas DataFrame.
        :return: Transformed DataFrame.
        """
        return (df.dropna()
                .assign(total=lambda x: x['price'] * x['quantity'])
                .query('total > 1000'))

