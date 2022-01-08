FROM pytorch/pytorch:latest

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt 

COPY app.py ./app.py
COPY features.py ./features.py
COPY policy_value_resnet.py ./policy_value_resnet.py
COPY checkpoints_checkpoint-004.pth ./checkpoints_checkpoint-004.pth

# Expose port 8080
EXPOSE 8080

ENTRYPOINT ["python3", "app.py"]