import click
from pathlib import Path
from webez.html_converter import convert_html_to_twig
from webez.css_converter import convert_css_to_scss, parse_variable_file

@click.group()
def main():
    """Convert HTML to Twig and CSS to SCSS."""
    pass

@main.command()
@click.argument('html_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
def html2twig(html_file, output_file):
    """Convert HTML file to Twig format."""
    try:
        html_content = Path(html_file).read_text(encoding='utf-8')
        twig_content = convert_html_to_twig(html_content)
        Path(output_file).write_text(twig_content, encoding='utf-8')
        click.echo(f"Successfully converted {html_file} to {output_file}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@main.command()
@click.argument('css_file', type=click.Path(exists=True))
@click.argument('variables_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
def css2scss(css_file, variables_file, output_file):
    """Convert CSS file to SCSS using variables from SCSS file."""
    try:
        css_content = Path(css_file).read_text(encoding='utf-8')
        variables_content = Path(variables_file).read_text(encoding='utf-8')
        
        variable_mapping = parse_variable_file(variables_content)
        scss_content = convert_css_to_scss(css_content, variable_mapping)
        
        Path(output_file).write_text(scss_content, encoding='utf-8')
        click.echo(f"Successfully converted {css_file} to {output_file}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == '__main__':
    main()
