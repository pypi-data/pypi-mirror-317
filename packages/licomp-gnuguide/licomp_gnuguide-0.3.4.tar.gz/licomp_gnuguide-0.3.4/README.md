# Licomp GNU Guide

Implementation of Licomp using [A Quick Guide to GPLv3](https://www.gnu.org/licenses/quick-guide-gplv3.html) providing compatibility:

* between an outbound license and inbound licenses
* when distributing a binary
* linking to (e.g. linking to a library) a licensed component
* the licensed component is unmodified

## A Quick Guide to GPLv3's original graph
![A Quick Guide to GPLv3's original graph](https://www.gnu.org/licenses/quick-guide-gplv3-compatibility.png)

## Licomp's graph
<img src="licomp-gnuguide.png" width="541" height="173">

## Introduction 

Licomp Gnuguide implements the [Licomp](https://github.com/hesa/licomp) api for communicating with the Licomp resources. For a better understanding of Licomp we suggest you read:

* [Licomp basic concepts](https://github.com/hesa/licomp/#licomp-concepts)
* [Licomp reply format](https://github.com/hesa/licomp/blob/main/docs/reply-format.md)

The various licomp resources below can be accessed as a group by:
* [licomp-toolkit](https://github.com/hesa/licomp-toolkit) - (`pip install licomp-toolkit`)

Licomp is used be the following compatibility resources:
* [licomp-hermione](https://github.com/hesa/licomp-hermione)
* [licomp-osadl](https://github.com/hesa/licomp-osadl)
* [licomp-proprietary](https://github.com/hesa/licomp-proprietary)
* [licomp-dwheeler](https://github.com/hesa/licomp-dwheeler)
* [licomp-gnuguide](https://github.com/hesa/licomp-gnuguide)

# Using Licomp GNU Guide

Since Licomp GNU Guide implements [Licomp](https://github.com/hesa/licomp) we refer to the Licomp guides (both cli and python api).

## Command line interface

See [Licomp Comand Line Interface](https://github.com/hesa/licomp/blob/main/docs/cli-guide.md)

_Note: the commmad line program for Licomp GNU Guide is called `licomp-gnuguide`._

## Python module

See [Licomp Python API](https://github.com/hesa/licomp/blob/main/docs/python-api.md)

# Installing Licomp GNU Guide

## From pypi.org

Licomp GNU Guide is available via [pypi.org](https://pypi.org/) at: [https://pypi.org/project/licomp-gnuguide/](https://pypi.org/project/licomp-gnuguide/).

To install, simply do the following:

```
$ pip install licomp-gnuguide
```

## From github

Installing from github assumes you already have `pip` installed.

```
$ git clone https://github.com/hesa/licomp-gnuguide
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
$ pip install .
```
