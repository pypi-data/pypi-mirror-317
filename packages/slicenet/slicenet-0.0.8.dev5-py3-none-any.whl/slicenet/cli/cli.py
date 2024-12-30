#!/usr/bin/env python3

import click
import os
import logging
from datetime import datetime
from importlib import metadata
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
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

def run_experiment(config_dir, out_dir):
    """Common function to run experiments from both CLI and shell"""
    # Create output directory if it doesn't exist
    os.makedirs(out_dir, exist_ok=True)
    
    # Create log file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(out_dir, f"slicenet-{timestamp}.log")
    
    logger = setup_logging(log_file)
    
    click.echo(f'Starting Slicenet Experiments with logs written to {log_file}')
    click.echo(f'Feel free to tail -f {log_file}')
    
    try:
        ctxMgr = ExperimentMgr()
        ctxMgr.loadExperimentsFromDir(in_dir=config_dir, out_dir=out_dir)
        ctxMgr.deployAndLaunch()
        ctxMgr.saveInference()
        logger.info("Experiments completed successfully")
        click.echo("Done.")
        return True
    except Exception as e:
        error_msg = f"Error running experiments: {str(e)}"
        logger.error(error_msg)
        raise click.ClickException(error_msg)

class SlicenetShell:
    def __init__(self):
        self.version = get_version()
        self.commands = {
            'run': self.run_command,
            'help': self.help_command,
            'exit': self.exit_command,
            'bye': self.exit_command
        }
        self.completer = WordCompleter(list(self.commands.keys()) + ['--config-dir', '--out-dir'])
        self.session = PromptSession(completer=self.completer)
        self.running = True

    def get_prompt(self):
        return f'slicenet-{self.version}> '

    def help_command(self, *args):
        """Display help information for available commands"""
        click.echo("\nAvailable commands:")
        click.echo("  run [--config-dir DIR] [--out-dir DIR]  Run experiments from configuration files")
        click.echo("  help                                    Show this help message")
        click.echo("  exit, bye                              Exit the shell\n")
        return True

    def exit_command(self, *args):
        """Exit the shell"""
        self.running = False
        return True

    def run_command(self, args):
        """Execute the run command with given arguments"""
        try:
            # Parse arguments
            config_dir = os.getcwd()
            out_dir = os.getcwd()
            
            i = 0
            while i < len(args):
                if args[i] in ['--config-dir', '-d'] and i + 1 < len(args):
                    config_dir = args[i + 1]
                    i += 2
                elif args[i] in ['--out-dir', '-o'] and i + 1 < len(args):
                    out_dir = args[i + 1]
                    i += 2
                else:
                    i += 1

            run_experiment(config_dir, out_dir)
            return True
        except click.ClickException as e:
            click.echo(f"Error: {str(e)}", err=True)
            return False
        except Exception as e:
            click.echo(f"Error: {str(e)}", err=True)
            return False

    def run(self):
        """Start the interactive shell"""
        click.echo(f"Welcome to Slicenet Interactive Shell v{self.version}")
        click.echo("Type 'help' for available commands, 'exit' or 'bye' to quit\n")

        while self.running:
            try:
                text = self.session.prompt(self.get_prompt())
                if not text.strip():
                    continue

                parts = text.split()
                command, args = parts[0].lower(), parts[1:]

                if command in self.commands:
                    self.commands[command](args)
                else:
                    click.echo(f"Unknown command: {command}")
                    click.echo("Type 'help' for available commands")

            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            except Exception as e:
                click.echo(f"Error: {str(e)}", err=True)

        click.echo("\nGoodbye!")

@click.group()
@click.version_option(version=get_version(), prog_name="Slicenet CLI", message='%(prog)s version %(version)s\nAuthor: Viswa Kumar')
def cli():
    """Slicenet CLI - A tool for running network slice experiments"""
    pass

@cli.command()
def shell():
    """Launch interactive shell mode"""
    shell = SlicenetShell()
    shell.run()

@cli.command()
@click.option('--config-dir', '-d', default=os.getcwd(),
              help='Directory containing experiment configuration files (default: current directory)')
@click.option('--out-dir', '-o', default=os.getcwd(),
              help='Output directory for logs and results (default: current directory)')
def run(config_dir, out_dir):
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
    run_experiment(config_dir, out_dir)

if __name__ == '__main__':
    cli()
