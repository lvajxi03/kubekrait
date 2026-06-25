from prompt_toolkit import Application
from prompt_toolkit.completion import Completer, Completion, PathCompleter, WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, VSplit
from prompt_toolkit.widgets import Frame, TextArea


class CommandCompleter(Completer):
    def __init__(self):
        self.commands = WordCompleter(
            ["open", "apply", "delete", "describe", "logs", "quit"],
            ignore_case=True,
        )
        self.path = PathCompleter(expanduser=True)

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        parts = text.split()

        # First word: command completion.
        if len(parts) == 0 or (len(parts) == 1 and not text.endswith(" ")):
            yield from self.commands.get_completions(document, complete_event)
            return

        command = parts[0].lower()

        # Commands expecting a filesystem path.
        if command in {"open", "apply"}:
            arg_start = text.rfind(" ") + 1
            arg_text = text[arg_start:]

            arg_document = type(document)(
                text=arg_text,
                cursor_position=len(arg_text),
            )

            yield from self.path.get_completions(arg_document, complete_event)
            return

        # Example: complete pod names after "logs".
        if command == "logs":
            current = "" if text.endswith(" ") else parts[-1]
            pods = ["nginx-abc123", "redis-0", "api-7d9f"]

            for pod in pods:
                if pod.startswith(current):
                    yield Completion(pod, start_position=-len(current))
            return

        # Example: delete resource type first, then resource name.
        if command == "delete":
            resource_types = ["pod", "deployment", "service", "configmap"]

            if len(parts) == 1 or (len(parts) == 2 and not text.endswith(" ")):
                current = "" if text.endswith(" ") else parts[-1]

                for resource_type in resource_types:
                    if resource_type.startswith(current):
                        yield Completion(
                            resource_type,
                            start_position=-len(current),
                        )
                return

            resource = parts[1]
            current = "" if text.endswith(" ") else parts[-1]

            names_by_resource = {
                "pod": ["nginx-abc123", "redis-0", "api-7d9f"],
                "deployment": ["nginx", "api", "worker"],
                "service": ["nginx", "redis", "api"],
                "configmap": ["app-config", "kube-root-ca.crt"],
            }

            for name in names_by_resource.get(resource, []):
                if name.startswith(current):
                    yield Completion(name, start_position=-len(current))


kb = KeyBindings()

pods = TextArea(
    text="Pods\nnginx-abc123\nredis-0\napi-7d9f",
    focusable=True,
)

details = TextArea(
    text="Details\nSelect something...",
    focusable=True,
)

logs = TextArea(
    text="Logs\n",
    focusable=True,
)

command = TextArea(
    height=1,
    prompt=": ",
    multiline=False,
    completer=CommandCompleter(),
    complete_while_typing=False,
)

focusables = [pods, details, logs, command]


@kb.add("c-w")
def switch_focus(event):
    layout = event.app.layout

    for i, widget in enumerate(focusables):
        if layout.has_focus(widget):
            layout.focus(focusables[(i + 1) % len(focusables)])
            return

    layout.focus(command)


@kb.add("tab")
def tab_completion(event):
    # Tab should trigger completion in the command line.
    if event.app.layout.has_focus(command):
        buff = command.buffer

        if buff.complete_state:
            buff.complete_next()
        else:
            buff.start_completion(select_first=False)
    else:
        switch_focus(event)


@kb.add("s-tab")
def previous_completion(event):
    if event.app.layout.has_focus(command):
        buff = command.buffer

        if buff.complete_state:
            buff.complete_previous()


@kb.add("enter")
def accept_command(event):
    if not event.app.layout.has_focus(command):
        return

    line = command.buffer.text.strip()
    if not line:
        return

    logs.buffer.insert_text(f"\n> {line}")

    if line == "quit":
        event.app.exit()
        return

    if line.startswith("apply "):
        path = line.removeprefix("apply ").strip()
        logs.buffer.insert_text(f"\nApplying file: {path}")

    elif line.startswith("open "):
        path = line.removeprefix("open ").strip()
        logs.buffer.insert_text(f"\nOpening file: {path}")

    elif line.startswith("logs "):
        pod = line.removeprefix("logs ").strip()
        logs.buffer.insert_text(f"\nShowing logs for pod: {pod}")

    elif line.startswith("delete "):
        logs.buffer.insert_text(f"\nDeleting: {line.removeprefix('delete ').strip()}")

    else:
        logs.buffer.insert_text("\nUnknown command")

    command.buffer.reset()


@kb.add("c-c")
@kb.add("c-q")
def exit_(event):
    event.app.exit()


root = HSplit([
    VSplit([
        Frame(pods, title="Pods"),
        Frame(details, title="Details"),
    ]),
    Frame(logs, title="Logs"),
    Frame(command, title="Command"),
])

app = Application(
    layout=Layout(root, focused_element=command),
    key_bindings=kb,
    full_screen=True,
    mouse_support=True,
)

if __name__ == "__main__":
    app.run()

