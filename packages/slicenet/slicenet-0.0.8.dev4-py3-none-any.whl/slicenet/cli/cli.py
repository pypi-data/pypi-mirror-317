#!/usr/bin/env python3

import click
import os
import logging
from datetime import datetime
from importlib import metadata
from ..utils.experimentMgr import ExperimentMgr

def setup_logging(log_file):
    logger = logging.getLogger('slicenet-cli')
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(name)s %(module)s %(levelname)s: %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.INFO,
        filename=log_file
    )
    return logger

def get_version():
    return metadata.version('slicenet')

@click.group()
@click.version_option(version=get_version(), prog_name="Slicenet CLI", message='%(prog)s version %(version)s\nAuthor: Viswa Kumar')
def cli():
    """Slicenet CLI - A tool for running network slice experiments"""
    pass

@cli.command()
@click.option('--config-dir', '-d', default=os.getcwd(),
              help='Directory containing experiment configuration files (default: current directory)')
@click.option('--out-dir', '-o', default=os.getcwd(),
              help='Output directory for logs and results (default: current directory)')
@click.option('--log-file', '-l', default=None,
              help='Log file path (default: slicenet_YYYYMMDD_HHMMSS.log)')
def run(config_dir, out_dir, log_file):
    """Run network slice experiments based on configuration files.
    
    This command loads experiment configurations from the specified config-dir,
    executes the experiments, and saves logs and results to the out-dir.
    
    The command will:
    1. Create a timestamped log file in the output directory
    2. Load and validate experiment configurations
    3. Deploy and launch the experiments
    4. Save inference results
    
    Example usage:
    \b
    # Run with default directories (current directory)
    $ slicenet run
    
    # Specify config and output directories
    $ slicenet run --config-dir ./configs --out-dir ./results
    """
    
    # Create output directory if it doesn't exist
    os.makedirs(out_dir, exist_ok=True)
    
    if not log_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(out_dir, f"slicenet-{timestamp}.log")
    
    logger = setup_logging(log_file)
    
    print(f'Starting Slicenet Experiments with logs written to {log_file}')
    print(f'Feel free to tail -f {log_file}')
    
    try:
        ctxMgr = ExperimentMgr()
        ctxMgr.loadExperimentsFromDir(in_dir=config_dir, out_dir=out_dir)
        ctxMgr.deployAndLaunch()
        ctxMgr.saveInference()
        logger.info("Experiments completed successfully")
        print("Done.")
    except Exception as e:
        logger.error(f"Error running experiments: {str(e)}")
        raise click.ClickException(str(e))

if __name__ == '__main__':
    cli()
