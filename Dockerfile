FROM python:slim

COPY . .

# Note to self - The below gives an example of best practices for Docker Security

# ENV USERNAME=dis-project
# ENV WORKING_DIR=/DISProject
# WORKDIR ${WORKING_DIR}
# RUN groupadd ${USERNAME} && \
#     useradd -m -g ${USERNAME} -d /home/${USERNAME} ${USERNAME}
# ## Changes owndership of WORKING_DIR and its contents
# RUN chown -R ${USERNAME}:${USERNAME} ${WORKING_DIR}
# ## This gives the user and group (u and g) read, write, and execute permissions to the working directory
# RUN chmod -R u=rwx,g=rwx ${WORKING_DIR}
# ## Switches to the new user
# USER ${USERNAME}
# ## Adds the given argument to the PATH so executables installed can be run easily
# ENV PATH "$PATH:/home/${USERNAME}/.local/bin"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_APP=flaskr

EXPOSE 5000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]