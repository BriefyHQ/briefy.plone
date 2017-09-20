FROM briefy/plone:5.0.8
MAINTAINER Briefy <developers@briefy.co>

USER root

COPY ./docker.cfg /plone/instance/docker.cfg
COPY setup.* *.rst MANIFEST.in /plone/instance/src/briefy.plone/
COPY src /plone/instance/src/briefy.plone/src
RUN mkdir -p /home/plone/.aws
COPY ./aws_config /home/plone/.aws/config

RUN chown -R plone:plone /plone /home/plone

USER plone

RUN bin/buildout -Nc docker.cfg
