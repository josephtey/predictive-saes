import os
from datetime import datetime
import sys

sys.path.append("../")
from encoder_sae.data_preparation.embedding_chunks.embed_chunks import embed_chunks
from encoder_sae.training_sae.train_sae import train_sae
from encoder_sae.feature_extraction.interp_sae import interp_sae
import argparse
import wandb


def main(args):
    wandb.init(
        # set the wandb project where this run will be logged
        project="auto-ed-coder",
        # track hyperparameters and run metadata
        config={
            **args,
            "type": "train_sae",
        },
    )

    # Define the run name and timestamp
    RUN_NAME = args["run_name"]
    TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Define the output directory
    OUTPUT_DIR = f"training_sae/saes/{RUN_NAME}_{TIMESTAMP}"

    # TRAIN SAE
    train_sae(
        sentences_file=args["sentences_file"],
        embeddings_file=args["embeddings_file"],
        run_folder=OUTPUT_DIR,
        batch_size=args["batch_size"],
        dimensions=args["dimensions"],
        sparsity_alpha=args["sparsity_alpha"],
        lr=args["lr"],
        num_epochs=args["num_epochs"],
        sparsity_scale=args["sparsity_scale"],
        wandb=wandb,
    )

    wandb.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the full pipeline")
    parser.add_argument(
        "--run_name", type=str, default="final_one", help="Name of the run"
    )
    parser.add_argument(
        "--model_name",
        type=str,
        help="Name of the model in HF",
    )
    parser.add_argument(
        "--sentences_file",
        type=str,
        required=True,
        help="Path to the input CSV file containing sentences",
    )
    parser.add_argument(
        "--embeddings_file",
        type=str,
        required=True,
        help="Path to the embeddings file",
    )
    parser.add_argument(
        "--batch_size", type=int, default=512, help="Batch size for training"
    )
    parser.add_argument(
        "--dimensions", type=int, default=768, help="Dimensions of the input data"
    )
    parser.add_argument(
        "--sparsity_alpha", type=float, default=1, help="Sparsity alpha parameter"
    )
    parser.add_argument("--lr", type=float, default=0.00001, help="Learning rate")
    parser.add_argument(
        "--num_epochs", type=int, default=1, help="Number of epochs for training"
    )
    parser.add_argument(
        "--sparsity_scale", type=float, default=1, help="Sparsity scale parameter"
    )
    
    args = parser.parse_args()
    main(vars(args))  # Convert Namespace object to a dictionary
