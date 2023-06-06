#!/usr/bin/env python3
import os

import aws_cdk as cdk

from url_short.url_short_stack import UrlShortStack, TrafficStack


app = cdk.App()
UrlShortStack(app, "UrlShortStack")
TrafficStack(app,  "test-ping")

app.synth()
