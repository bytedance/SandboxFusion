FROM volcengine/sandbox-fusion:server-20250609

# Installing python dependencies
COPY python-dependencies.txt* .
RUN if [ -s python-dependencies.txt ]; then \
      conda install -y -n sandbox-runtime $(cat python-dependencies.txt); \
    fi

# Installing node dependencies
COPY node-dependencies.txt* runtime/node
RUN if [ -s runtime/node/node-dependencies.txt ]; then \
      cd runtime/node && npm install $(cat node-dependencies.txt); \
    fi

# Installing java dependencies
COPY java-dependencies.txt* runtime/java
RUN if [ -s runtime/java/java-dependencies.txt ]; then \
      cd runtime/java && wget -P lib -i java-dependencies.txt; \
    fi

# Installing ruby dependencies
COPY ruby-dependencies.txt* .
RUN if [ -s ruby-dependencies.txt ]; then \
      gem install $(cat ruby-dependencies.txt); \
    fi

COPY sandbox/runners/major.py sandbox/runners/major.py
