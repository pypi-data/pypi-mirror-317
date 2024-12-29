#!/usr/bin/env python3

import click
import os
import logging
from datetime import datetime
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

@click.group()
def cli():
    """Slicenet CLI - A tool for running network slice experiments"""
    pass

@cli.command()
@click.option('--config-dir', '-d', default=os.getcwd(),
              help='Directory containing experiment configuration files')
@click.option('--log-file', '-l', default=None,
              help='Log file path (default: slicenet_YYYYMMDD_HHMMSS.log)')
def run(config_dir, log_file):
    """Run experiments from configuration files in the specified directory"""
    if not log_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"slicenet_{timestamp}.log"
    
    logger = setup_logging(log_file)
    
    print(f'Starting Slicenet Experiments with logs written to {log_file}')
    print(f'Feel free to tail -f {log_file}')
    
    try:
        ctxMgr = ExperimentMgr()
        ctxMgr.loadExperimentsFromDir(in_dir=config_dir)
        ctxMgr.deployAndLaunch()
        ctxMgr.saveInference()
        logger.info("Experiments completed successfully")
        print("Done.")
    except Exception as e:
        logger.error(f"Error running experiments: {str(e)}")
        raise click.ClickException(str(e))

if __name__ == '__main__':
    cli()
