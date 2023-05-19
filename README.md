# Memento - Visual Memory Test

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

1. As a First Time Visitor, 

### Returning Visitor Goals

1. As a Returning Visitor, 

### Frequent User Goals

1. As a Frequent User,

## Design
- Colors
- Loading Text

# Flowchart
![DoubleTake Lucid Flowchart]()

# Features

## Main Menu

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
