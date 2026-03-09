
#!/bin/bash

## Prepare
cd "$(dirname "$0")"

## Setup script
# brew install ruby   
# export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
# gem install bundler
# bundle install

## Compile

export PATH="/opt/homebrew/opt/ruby/bin:$PATH"

bundle exec jekyll serve
