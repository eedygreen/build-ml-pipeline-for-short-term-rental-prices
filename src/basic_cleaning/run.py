#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import os
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(project="nyc_airbnb", job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    try:
        logger.info("Downloading artifact...")
        artifact_local_path = run.use_artifact(args.input_artifact).file()
        
        df = pd.read_csv(artifact_local_path)

        logger.info("Dropping duplicates...")
        df = df.drop_duplicates().reset_index(drop=True)

        logger.info("Feature engineering...")
        df['price'] = df['price'].fillna(0)
        df_filtered = df[df['price'].between(args.min_price, args.max_price, inclusive='both')]
        
        idx = (
            df_filtered['longitude'].between(-74.25, -73.50) &
            df_filtered['latitude'].between(40.5, 41.2)
        )
        df_filtered = df_filtered[idx].reset_index(drop=True).copy()
        
        filename = "clean_sample.csv"
        logger.info(f"Saving new dataframe to file {filename}")
        df_filtered.to_csv(filename, index=False)
        logger.info(f"file {filename} created!")
    except ValueError as err:
        logger.error(f"basic_cleaning: error {err}")
    except Exception as e:
        logger.error(f"basic_cleaning: error {e}", exc_info=True)
    
    try: 
        artifact = wandb.Artifact(
            args.output_artifact,
            type=args.output_type,
            description=args.output_description,
        )
        artifact.add_file("clean_sample.csv")

        logger.info("Logging artifact")
        run.log_artifact(artifact)
        logger.info("Logged artifact!")

        os.remove(filename)
    except ValueError as err:
        logger.error(f"basic_cleaning: error {err}")
    except Exception as e:
        logger.error(f"basic_cleaning: error {e}", exc_info=True)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="A very basic data cleaning"
    )

    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Fully qualified name of the artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of the produced artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of the artifact to be produced",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=int,
        help="Minimum price to be filtered",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=int,
        help="Maximum price to be filtered",
        required=True
    )


    args = parser.parse_args()

    go(args)
