# All in one CLI using Docker

Docli simulates CLIs executables using Docker images. With Docli it's faster to install and remove executables, and prevents installation of several library into your workspace.

Docli CLI was STRONGLY based (not to say copied) on [rbenv](https://github.com/rbenv/rbenv) CLI and documentation.

## How It Works

At a high level, Docli intercepts services excutables commands using shim
executables injected into your `PATH`, determines which Docker image to use,
mounts your home into Docker container, and passes your commands to the
container entrypoint.

### Understanding Shims

Docli works by inserting a directory of _shims_ at the front of your
`PATH`:

    ~/.docli/shims:/usr/local/bin:/usr/bin:/bin

Through a process called _rehashing_, Docli maintains shims in that
directory to match every command across every CLI command registered.

Shims are symbolic link that simply pass your command along
to Docli. So with Docli installed, when you run, for example, `terraform`,
your operating system will do the following:

* Search your `PATH` for an executable file named `terraform`
* Find the Docli shim named `terraform` at the beginning of your `PATH`
* Run the shim named `terraform`, which in turn passes the command along
  to Docli

### Choosing the Docker image

When you execute a shim, Docli determines which Docker image to use by
reading the file `.bashrc` from your current file and the `.bashrc` file
from it's parent directory, and so on, until it gets to your $HOME directory.

The higher level directory takes precedence. For example, if you have terraform
configured in global context ($HOME) with the image `hashicorp/terraform:0.12.13`,
and another terraform in the local context ($PWD) with `hashicorp/terraform:0.11.14`,
as you expect, Docli will use the image `hashicorp/terraform:0.11.14` to execute your
command.

## Installation

  **Note**: For the time being Docli requires python 2 installed to work properly.

This will get you going with the latest version of Docli without needing
a systemwide install.

1. Clone Docli into `~/.docli`.

    ~~~ sh
    $ git clone https://github.com/mpelos/docli.git ~/.docli
    ~~~

2. Add `~/.docli/bin` to your `$PATH` for access to the `docli`
   command-line utility.

   * For **bash**:
     ~~~ bash
     $ echo 'export PATH="$HOME/.docli/bin:$PATH"' >> ~/.bash_profile
     ~~~

   * For **Ubuntu Desktop**:
     ~~~ bash
     $ echo 'export PATH="$HOME/.docli/bin:$PATH"' >> ~/.bashrc
     ~~~

   * For **Zsh**:
     ~~~ zsh
     $ echo 'export PATH="$HOME/.docli/bin:$PATH"' >> ~/.zshrc
     ~~~

   * For **Fish shell**:
     ~~~ fish
     $ set -Ux fish_user_paths $HOME/.docli/bin $fish_user_paths
     ~~~

3. Set up Docli in your shell.

   ~~~ sh
   $ ~/.docli/bin/docli init
   ~~~

   Follow the printed instructions to set up Docli shell integration.

4. Restart your shell so that PATH changes take effect. (Opening a new
   terminal tab will usually do it.)

## Registering new CLIs services

### Global context

The `docli add` command, for default, will add a CLI service configuration
in your global `$HOME/.doclirc` file.

   Usage:
   ~~~ sh
   $ docli add <cli-name> <docker-image> [--entrypoint=<docker-image-entrypoint>]
   ~~~

Some executables requires entrypoints to work properly, and others like `terraform`
already have the proper entrypoint configured into the image.

   Example:
   ~~~ sh
   # add executable without entrypoint
   $ docli add terraform hashicorp/terraform

   # add executable with entrypoint
   $ docli add gsutil google/cloud-sdk:alpine --entrypoint=gsutil
   ~~~

### Local context

The `docli add` command, accepts `--local` flag. will add a CLI service configuration
in the `.doclirc` file in your current directory. This executable will work in this
directory and its descendants.

   Usage:
   ~~~ sh
   $ docli add <cli-name> <docker-image> --local [--entrypoint=<docker-image-entrypoint>]
   ~~~

   Example:
   ~~~ sh
   # add executable with entrypoint
   $ docli add gcloud google/cloud-sdk:alpine --local --entrypoint=gsutil
   ~~~

## Development

Please feel free to submit pull requests and file bugs on the [issue
tracker](https://github.com/mpelos/docli/issues).
