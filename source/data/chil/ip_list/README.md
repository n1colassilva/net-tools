# Chil data

## Data for chil -> ip_list

There are some important files you should avoid touching:
    - `example.toml` - Example is just an example of what a TOML for chil should be like
    - `test.toml` - Test is a file used for testing
Everything else is free game.

## How to make a chil data file

### What is Toml

Chil data files are made in TOML (Tom's Obvious Markup Language), you can read more about it [here](https://toml.io/en/)

### Structure

Chil data files in their TOML form are an array of tables containing key-value pairs

- The top level table is called ip_adresses

- ip_adresses contain entries

- entries contain ip adress specifications, such as
  - **address** (str) - The address, for obvious reasons entries **must** contain it
    - The IP addresses should be in this (ipv4) format:
      "xxx.xxx.xxx"
  - **name** (str, optional) -  A name you can give to the address
    - "Sharepoint"
    - "Test server"
    - "Lab"
    - "home"
  - **description** (str,optional) - A description you can give
    - "Server for file sharing in local network"
    - "Server for short experiments"
    - "Machine for home experiments, used to access test server"
    - "Main home machine"

these entries can either be created, modified or deleted in net-tools using `chil` itself or by hand
> for more information run net-tools and use `chil help`

The syntax is as follows

```TOML
[ip_addresses] # the top level table

[[ip_addresses.entry]] # each entry needs to be prepended with the name of the top level table, all entries are named the same, do not deviate.
address = "192.168.0.1" # IPv4 address
name = "home" # Optional name
description = "main home machine" # Optional description

[[ip_addresses.entry]] #another entry
address = "192.168.0.2"
```

Additionally, if you do write comments and want those to be preserved keep writing the file by hand or set it as read-only.
