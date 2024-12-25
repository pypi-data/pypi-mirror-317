# LLMux

Large language model inference for power users. At the current development stage it is more or less a ChatGPT CLI/TUI.

## Get started

### Install

`pipx install git+https://github.com/danisztls/llmux`

### Get an API key

Go to [platform.openai.com](https://platform.openai.com) and log-in with your OpenAI account (register if you don't have one). Click on your name initial in the top-right corner, then select _"View API keys"_. Finally click on _"Create new secret key"_. That's it.

You may also need to add a payment method, clicking on _Billing --> Payment methods_. New accounts should have some free credits, but adding a payment method may still be mandatory. For pricing, check [this page](https://openai.com/pricing).

### Configure API key

There are three alternatives.

a. Export the key as an env var: `export OPENAI_API_KEY="<YOUR_KEY>"`

b. Create a global configuration at `$XDG_CONFIG_HOME/llmux/config.yaml` or a local at `./llmux.yaml`:

```yaml
api-key: "YOUR_KEY"
```

c. Use the command line option `--key <YOUR_KEY>`.

The configuration priority order is: _Command line option > Environment variable > Local configuration file > Global configuration file_.

### Usage

Run `llmux`. Then just chat!

The number next to the prompt is the [tokens](https://platform.openai.com/tokenizer) used in the conversation at that point.

Use the `/q` command to quit and show the number of total tokens used and an estimate of the expense for that session, based on the specific model in use.

## Advanced configuration

```yaml
model: "gpt-3.5-turbo"
markdown: false
max_tokens: 500
temperature: 1
```

### Models

ChatGPT CLI, by default, uses the original `gpt-3.5-turbo` model. In order to use other ChatGPT models, edit the `model` parameter in the _config.yml_ file ore use the `--model` command line option. Here is a list of all the available options:

| Name                 | Pricing (input token) | Pricing(output token) |
| -------------------- | --------------------- | --------------------- |
| `gpt-3.5-turbo`      | 0.0015                | 0.002                 |
| `gpt-3.5-turbo-0613` | 0.0015                | 0.002                 |
| `gpt-3.5-turbo-16k`  | 0.003                 | 0.004                 |
| `gpt-4`              | 0.03                  | 0.06                  |
| `gpt-4-0613`         | 0.03                  | 0.06                  |
| `gpt-4-32k`          | 0.06                  | 0.12                  |
| `gpt-4-32k-0613`     | 0.06                  | 0.12                  |

Pricing is calculated as $/1000 tokens.

Check [this page](https://platform.openai.com/docs/models) for the technical details of each model.

## Advanced usage

### Multiline input

Add the `--multiline` (or `-ml`) flag in order to toggle multi-line input mode. In this mode use `Alt+Enter` or `Esc+Enter` to submit messages.

### Context

Use the `--context <FILE PATH>` command line option (or `-c` as a short version) in order to provide the model an initial context (technically a _system_ message for ChatGPT). For example:

`llmux --context notes.txt`

Both absolute and relative paths are accepted. Note that this option can be specified multiple times to give multiple files for context. Example:

`llmux --context notes-from-thursday.txt --context notes-from-friday.txt`

### Restoring previous sessions

ChatGPT CLI saves all the past conversations (including context and token usage) in `$XDG_DATA_HOME/llmux`. In order to restore a session the `--restore <YYYYMMDD-hhmmss>` (or `-r`) option is available. For example:

`llmux --restore 20230728-162302` restores the session from the `$XDG_DATA_HOME/llmux/session-20230728-162302.json` file. Then the chat goes on from that point.

It is also possible to use the special value `last`:

`llmux --restore last`

In this case it restores the last chat session, without specifying the timestamp.

Note that, if `--restore` is set, it overwrites any `--context` option.
