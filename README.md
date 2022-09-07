# Sunduki - MineRL Artificial ~~intelligence~~

## Repo Structure

- **bin** - binstubs for the project
- **src** - *herobrain* and custom agent logic
- **constants** - utils with helper functions and variables
- **weights** - weights for TensorFlow model
- **main.py** - project's main function that starts the render

## Setup

Be sure to execute commands in zsh (Binstubs not optimised for Windows. I've tried...)

1. First make sure you have JDK 8 installed on your system.
   - **Windows**:
      Windows JDK8 installer can be found on unofficial sites. (Oracle no longer supports old versions of JDK unfortunately) 
   - **MacOS**:
      On MacOS you can use *homebrew* and *AdoptOpenJDK8* to install java8.
      ```
      brew tap AdoptOpenJDK/openjdk
      brew install --cask adoptopenjdk8
      ```
   - **Debian based systems**:
      ```
      sudo add-apt-repository ppa:openjdk-r/ppa
      sudo apt-get update
      sudo apt-get install openjdk-8-jdk
      ```
2. Run `bin/setup`.

## Running Application

This project includes my own binstubs so feel free to use them ;)

Here is a list with some of them:

1. If you'r using VScode run `bin/code` to open project in editor.
2. Run `bin/start` to run render.

See [bin/folder](bin) for available binstubs.

## Docs

### MineRL 
 Library that implements OpenAI Gym functionality for reinforcement learning and provides us with the neccessary data for training the neural network both by reinforcement and with supervisor.

### TensorFlow 
  an end-to-end open source platform for machine learning. It lets researchers push the state-of-the-art in ML and developers easily build and deploy ML powered applications.

### Gym
  an open source Python library for developing and comparing reinforcement learning algorithms by providing a standard API to communicate between learning algorithms and environments, as well as a standard set of environments compliant with that API


---