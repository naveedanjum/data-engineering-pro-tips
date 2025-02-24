import os
import pandas as pd
import polars as pl
from multiprocessing import Pool
from utils import DataUtils

# Sample data for testing
TEST_CSV = "test_data.csv"
TEST_PARQUET = "test_data.parquet"

# Create sample test data
sample_data = pd.DataFrame({
    "id": range(1, 6),
    "category": ["A", "B", "A", "B", "C"],
    "price": [100, 200, 150, 250, 300],
    "quantity": [2, 3, 4, 5, 6]
})

# Save test data as CSV
sample_data.to_csv(TEST_CSV, index=False)


def process_chunk(chunk):
    """Function to process a chunk of the dataframe."""
    return chunk.groupby("category").sum()


def test_read_large_file():
    """Test generator-based file reading."""
    print("\n✅ Testing read_large_file()...")
    lines = list(DataUtils.read_large_file(TEST_CSV))
    assert len(lines) > 0, "File reading failed!"
    print("✔ Passed!")


def test_optimize_dataframe():
    """Test dataframe memory optimization."""
    print("\n✅ Testing optimize_dataframe()...")

    before_memory = sample_data.memory_usage().sum()
    optimized_df = DataUtils.optimize_dataframe(sample_data.copy())
    after_memory = optimized_df.memory_usage().sum()

    print(f"Before Optimization: {before_memory / 1024:.4f} KB")
    print(f"After Optimization: {after_memory / 1024:.4f} KB")

    assert after_memory < before_memory, "Memory optimization failed!"
    print("✔ Passed!")


def test_convert_csv_to_parquet():
    """Test CSV to Parquet conversion."""
    print("\n✅ Testing convert_csv_to_parquet()...")
    DataUtils.convert_csv_to_parquet(TEST_CSV, TEST_PARQUET)
    assert os.path.exists(TEST_PARQUET), "Parquet conversion failed!"
    print("✔ Passed!")


def test_method_chaining():
    """Test Pandas method chaining."""
    print("\n✅ Testing chain_transformations()...")
    transformed_df = DataUtils.chain_transformations(sample_data.copy())
    assert "total" in transformed_df.columns, "Method chaining failed!"
    print("✔ Passed!")


def test_parallel_processing():
    """Test multiprocessing for ETL."""
    print("\n✅ Testing multiprocessing...")

    chunks = [sample_data.iloc[:3], sample_data.iloc[3:]]

    with Pool(2) as pool:
        results = pool.map(process_chunk, chunks)

    final_df = pd.concat(results)

    assert not final_df.empty, "Multiprocessing ETL failed!"
    print("✔ Passed!")


def test_polars_processing():
    """Test loading and filtering with Polars."""
    print("\n✅ Testing Polars high-performance processing...")
    df_polars = pl.read_parquet(TEST_PARQUET)
    filtered_df = df_polars.filter(pl.col("price") > 150)
    assert len(filtered_df) > 0, "Polars processing failed!"
    print("✔ Passed!")


if __name__ == "__main__":
    test_read_large_file()
    test_optimize_dataframe()
    test_convert_csv_to_parquet()
    test_method_chaining()
    test_parallel_processing()
    test_polars_processing()

    # Cleanup test files
    os.remove(TEST_CSV)
    os.remove(TEST_PARQUET)

    print("\n🎯 All tests passed successfully!")
