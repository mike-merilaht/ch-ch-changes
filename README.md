# ch-ch-changes
[Keep A Changelog](https://keepachangelog.com/en/1.0.0/) + [GitFlow](https://nvie.com/posts/a-successful-git-branching-model/) accountability buddy

## Recommendations

I recommend that you also add the following aliases to your bash profile of choice

```
alias gc="<PATH_TO_CHECK_CHANGELOG.sh> && git commit -m $1"
alias changelog="<PATH_TO_CHANGELOG.py> --ticket-url-prefix='<URL_HERE>'"
```

`gc` will not let you commit without having a valid entry for the ticket you are working on. This uses the git flow format for branches, i.e bug/XX-XXXX-..., to get the ticket.

`changelog` is a nice shortcut for putting the ticket url into ever call to this command. This is more useful when using 1 ticketing system.

## Development

Ensure you run black on the code before commiting

```
python -m black .
```