#!/usr/bin/env python
import click


class ChangeLogModifier:
    sections = {
        "add": {"prefix": "### Added", "index": -1},
        "change": {"prefix": "### Changed", "index": -1},
        "fix": {"prefix": "### Fixed", "index": -1},
        "remove": {"prefix": "### Removed", "index": -1},
        "dev": {"prefix": "### Dev", "index": -1},
    }

    def _parse_changelog(self, filepath):
        lines = []
        releases = -1
        with open(filepath, "r") as file:
            index = 0
            for line in file:
                lines.append(line)
                if (
                    line.startswith("## [") and not line.startswith("## [Unreleased]")
                ) and releases == -1:
                    releases = index
                if (
                    line.startswith(self.sections["add"]["prefix"])
                    and self.sections["add"]["index"] == -1
                    and releases == -1
                ):
                    self.sections["add"]["index"] = index

                if (
                    line.startswith(self.sections["fix"]["prefix"])
                    and self.sections["fix"]["index"] == -1
                    and releases == -1
                ):
                    self.sections["fix"]["index"] = index

                if (
                    line.startswith(self.sections["change"]["prefix"])
                    and self.sections["change"]["index"] == -1
                    and releases == -1
                ):
                    self.sections["change"]["index"] = index

                if (
                    line.startswith(self.sections["remove"]["prefix"])
                    and self.sections["remove"]["index"] == -1
                    and releases == -1
                ):
                    self.sections["remove"]["index"] = index

                if (
                    line.startswith(self.sections["dev"]["prefix"])
                    and self.sections["dev"]["index"] == -1
                    and releases == -1
                ):
                    self.sections["dev"]["index"] = index

                index = index + 1
        return lines

    def _create_new_line(self, text, ticket, ticket_url_prefix):
        ticket_url = f"{ticket_url_prefix}{ticket}"
        markdown_link = f"[{ticket}]({ticket_url})"
        markdown_line = f"- {text} ({markdown_link})\n"
        return markdown_line

    def _add_new_line(self, lines, new_line, section):
        current_line_index = self.sections[section]["index"]

        if current_line_index == -1:
            raise Exception(f'Section for "{section}" not found in changelog.')

        for current_line in lines[current_line_index + 1 :]:
            if current_line.strip() == "":
                current_line_index = current_line_index + 1
                break

            # If we hit the start of a previous release
            # Probably should error here.
            if current_line.startswith("##"):
                raise Exception(f'Section for "{section}" not found in changelog.')

            current_line_index = current_line_index + 1

        lines.insert(current_line_index, new_line)
        return lines

    def add(self, ticket, text, section, filepath, ticket_url_prefix):
        new_line = self._create_new_line(text, ticket, ticket_url_prefix)
        lines = self._parse_changelog(filepath)
        lines = self._add_new_line(lines, new_line, section)

        with open(filepath, "w") as file:
            file.writelines(lines)


@click.command()
@click.option(
    "--ticket", help="JIRA ticket number", prompt="JIRA Ticket Number (e.g XX-XXXX)"
)
@click.option("--text", help="Changelog line", prompt="Text for changelog")
@click.option(
    "--section",
    type=click.Choice(["add", "fix", "change", "remove", "dev"]),
    default="change",
    help="What kind of item to add to the changelog.",
    prompt="Entry section",
)
@click.option(
    "--filepath",
    help="Path to changelog (defaults to ./CHANGELOG.md)",
    default="CHANGELOG.md",
)
@click.option(
    "--ticket-url-prefix",
    help="Example 'https://XYZ.atlassian.net/browse/'",
    prompt=True,
)
def main(ticket, text, section, filepath, ticket_url_prefix):
    ChangeLogModifier().add(ticket, text, section, filepath, ticket_url_prefix)


if __name__ == "__main__":
    main()
