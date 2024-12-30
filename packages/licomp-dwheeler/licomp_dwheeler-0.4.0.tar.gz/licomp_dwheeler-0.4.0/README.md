# licomp-dwheeler

Implementation of Licomp using David Wheeler's [license compatibility graph](https://dwheeler.com/essays/floss-license-slide.html) providing compatibility:

* between an outbound license and inbound licenses
* when distributing a binary
* linking to (e.g. linking to a library) a licensed component
* the licensed component is unmodified

## David Wheeler's original graph
![David Wheeler's original graph](https://dwheeler.com/essays/floss-license-slide-image.png)

## Licomp's graph
<img src="licomp-dwheeler.png" width="343" height="365">

## Introduction 

Licomp dwheeler implements the [Licomp](https://github.com/hesa/licomp) api for communicating with the Licomp resources. For a better understanding of Licomp we suggest you read:

* [Licomp basic concepts](https://github.com/hesa/licomp/#licomp-concepts)
* [Licomp reply format](https://github.com/hesa/licomp/blob/main/docs/reply-format.md)

The various licomp resources below can be accessed as a group by:
* [licomp-toolkit](https://github.com/hesa/licomp-toolkit) - (`pip install licomp-toolkit`)

Licomp is used be the following compatibility resources:
* [licomp-hermione](https://github.com/hesa/licomp-hermione)
* [licomp-osadl](https://github.com/hesa/licomp-osadl)
* [licomp-proprietary](https://github.com/hesa/licomp-proprietary)
* [licomp-dwheeler](https://github.com/hesa/licomp-dwheeler)

# Using Licomp Dwheeler

Since Licomp Dwheeler implements [Licomp](https://github.com/hesa/licomp) we refer to the Licomp guides (both cli and python api).

## Command line interface

See [Licomp Comand Line Interface](https://github.com/hesa/licomp/blob/main/docs/cli-guide.md)

_Note: the commmad line program for Licomp Dwheeler is called `licomp-dwheeler`._

## Python module

See [Licomp Python API](https://github.com/hesa/licomp/blob/main/docs/python-api.md)

# Installing Licomp Dwheeler

## From pypi.org

Licomp Dwheeler is available via [pypi.org](https://pypi.org/) at: [https://pypi.org/project/licomp-dwheeler/](https://pypi.org/project/licomp-dwheeler/).


To install, simply do the following:

```
$ pip install licomp-dwheeler
```

## From github

Installing from github assumes you already have `pip` installed.

```
$ git clone https://github.com/hesa/licomp-dwheeler
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
$ pip install .
```
