# DoubleTake - A Python-based game of telephone

[DoubleTake](https://doubletake.herokuapp.com/) was developed for anyone who enjoys a twist on traditional telephone games.

In this game players will create chains of alternating questions and answers while attempting to unravel what previous players have said, often with unpredictable results.

# Table of Contents
+ [UX](#ux "UX")
  + [User Stories](#user-stories "User Stories")
  + [Design](#design "Design")
+ [Flowchart](#flowchart "Flowchart")
+ [Features](#features "Features")
  + [Main Menu](#main-menu "Main Menu")
  + [The Game](#the-game "The Game")
  + [Chain Viewer](#chain-viewer "Chain Viewer")
+ [Development](#development "Development")
  + [Heroku Deployment](#heroku-deployment "Heroku Deployment")
+ [Testing](#Testing "Testing")
  + [General Testing](#general-testing "General Testing")
  + [Validator Testing](#validator-testing "Validator Testing")
  + [Bugs Encountered](#bugs-encountered "Bugs Encountered")
+ [Credits](#credits "Credits")

# UX

## User stories

### First Time Visitor Goals

- As a first time visitor, I want to enjoy a simple text-based multiplayer game
- As a first time visitor, I want to quickly grasp how to play the game
- As a first time visitor, I want to see what came before my contribution after finishing a round

### Returning Visitor Goals

- As a returning visitor, I want to look at finished chains to see what my past contributions led up to
- As a returning visitor, I want to easily navigate through menus with minimal effort 
- As a returning visitor, I want to see if any new chains have been finished

## Design
- Certain words and phrases are colored to guide the user's eyes and make interaction more intuitive
  - As an example, questions and answers are consistently yellow/magenta throughout the game, while signatures always appear in cyan
  ![DoubleTake Colors](assets/images/doubletake-colors.png)

- As interacting with the spreadsheet through Google API may take a few seconds, subtle loading messages have been implemented to provide the user with some level of feedback while the application is working. 

# Flowchart
![DoubleTake Lucid Flowchart](assets/images/doubletake-lucidchart.png)

# Features

## Main Menu
- The main menu features a quick introductory blurb and instructions on how to play the game
## The Game

## Chain Viewer

# Development

## Heroku Deployment
The project was deployed as a Heroku App (Link [here](https://doubletake.herokuapp.com/)) using the following steps:
  1. 

# Testing

## Validator Testing

## Bugs Encountered

# Credits
Resources and tutorials used for developing this project:
-

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.
