import click

def prompt_from_list(prompt_text, options):
    """
    Display a numbered menu for a list of options and return the selected value.
    
    :param prompt_text: The question to display
    :param options: A list of valid string options
    :return: The selected option (string)
    """
    # Build numbered map
    numbered_options = {str(i): option for i, option in enumerate(options, start=1)}

    click.echo(prompt_text)
    for number, option in numbered_options.items():
        click.echo(f"{number}. {option}")

    choice_num = click.prompt(
        "Enter the number of your choice",
        type=click.Choice(numbered_options.keys(), case_sensitive=False)
    )

    return numbered_options[choice_num]