# Judgelet security

Running untrusted code poses a serious security risk if not handled well.

This page describes taken security measures, considerations and potential risks.

## Measures

To prevent potential unwanted consequences of running untrusted code, following is done:

- Judgelet runs as unprivileged user
- Judgelet runs in a separate network
- Judgelet does not know about any services out there whatsoever, it only accepts requests

## Considerations

- (For now) the code is not sandboxed
- Solution directories are not isolated

These measures are planned for implementation.

