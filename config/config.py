import os

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost/usac-store') 
JWT_SEED = os.environ.get('JWT_SECRET_KEY', 'y1ha3-vfPdSnm>qT&t:')