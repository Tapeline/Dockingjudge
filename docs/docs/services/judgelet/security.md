# Judgelet security

Running untrusted code poses a serious security risk if not handled well.

This page describes taken security measures, considerations and potential risks.

## Measures

To prevent potential unwanted consequences of running untrusted code, following is done:

- Judgelet runs as unprivileged user
- Judgelet runs in a separate network
- Judgelet does not know about any services out there whatsoever, it only accepts requests
- Every solution is run in a new [`bubblewrap`](https://github.com/containers/bubblewrap) 
  sandbox (by default), so every solution is isolated from others.

## Considerations

Though Dockingjudge uses Docker and bubblewrap, which **do** give some promises
regarding security:

> container process that runs is isolated in that it has 
> its own file system, its own networking, and its own 
> isolated process tree separate from the host
> 
> [_-- Docker docs_](https://docs.docker.com/engine/containers/run/)

> The maintainers of this tool believe that it does not,
> even when used in combination with typical software 
> installed on that distribution, allow privilege escalation.
> 
> [_-- Bubblewrap README.md_](https://github.com/containers/bubblewrap?tab=readme-ov-file#system-security)

it should be considered that their provided security may be not full.

For example, Judgelets _may_ be vulnerable for DoS attacks. As per bubblewrap README.md:

>  It may increase the ability of a logged in user to perform denial of service attacks, however.

