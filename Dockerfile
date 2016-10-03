FROM briefy/plone:latest
MAINTAINER Briefy <developers@briefy.co>

USER root

COPY ./docker.cfg /plone/instance/docker.cfg
COPY setup.* *.rst MANIFEST.in /plone/instance/src/briefy.plone/
COPY src /plone/instance/src/briefy.plone/src

RUN chown -R plone:plone /plone

USER plone

RUN mkdir -p /home/plone/.aws
COPY ./aws_config /home/plone/.aws/config

RUN bin/buildout -Nc docker.cfg
