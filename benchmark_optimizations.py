import pandas as pd
import polars as pl
import time
import psutil
import os
from multiprocessing import Pool
from utils import DataUtils

# Define file paths
CSV_FILE = "sample_data.csv"
PARQUET_FILE = "sample_data.parquet"


# Function to measure memory usage
def get_memory_usage():
    return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)  # MB


# Function to benchmark execution time
def benchmark(func, *args, **kwargs):
    start_time = time.time()
    start_mem = get_memory_usage()
    result = func(*args, **kwargs)
    end_time = time.time()
    end_mem = get_memory_usage()

    print(
        f"✅ {func.__name__} executed in {end_time - start_time:.4f} seconds | Memory Used: {end_mem - start_mem:.4f} MB")
    return result


# Regular Pandas approach (Non-Optimized)
def pandas_processing():
    df = pd.read_csv(CSV_FILE)
    df['total'] = df['price'] * df['quantity']
    df_filtered = df[df['total'] > 1000]
    return df_filtered


# Optimized Pandas processing using method chaining
def optimized_pandas_processing():
    df = pd.read_csv(CSV_FILE)
    return DataUtils.chain_transformations(df)


# Parallelized processing using multiprocessing
def parallel_processing():
    chunks = pd.read_csv(CSV_FILE, chunksize=5)
    with Pool(2) as pool:
        results = pool.map(DataUtils.optimize_dataframe, chunks)
    return pd.concat(results)


# Using Polars for high-performance processing
def polars_processing():
    df = pl.read_csv(CSV_FILE)
    df = df.with_columns((df['price'] * df['quantity']).alias('total'))
    return df.filter(pl.col("total") > 1000)


# Convert CSV to Parquet and process data from Parquet
def parquet_processing():
    DataUtils.convert_csv_to_parquet(CSV_FILE, PARQUET_FILE)
    df = pl.read_parquet(PARQUET_FILE)
    return df.filter(pl.col("sales") > 1000)


# Run Benchmarks
if __name__ == "__main__":
    print("\n📊 **Benchmarking Data Processing Approaches** 📊\n")

    benchmark(pandas_processing)  # Regular Pandas
    benchmark(optimized_pandas_processing)  # Optimized Pandas
    benchmark(parallel_processing)  # Multiprocessing Pandas
    benchmark(polars_processing)  # High-performance Polars
    benchmark(parquet_processing)  # Parquet optimized processing

    print("\n🎯 **Optimization Results Completed!** 🎯")
