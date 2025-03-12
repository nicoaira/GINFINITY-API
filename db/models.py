from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Embedding(Base):
    __tablename__ = "exon_embeddings"  # Updated to match your actual table name
    id = Column(Integer, primary_key=True, index=True)
    gene_id = Column(String(50), unique=True, index=True, nullable=False)
    gene_name = Column(String(255))
    transcript_id = Column(String(50))
    exon_id = Column(String(50))
    exon_number = Column(Integer)
    chr = Column(String(10))
    start = Column(Integer)
    end = Column(Integer)
    strand = Column(String(2))
    rna_sequence = Column(String(1024))
    rna_ss = Column(String(1024), nullable=False)
    seq_len = Column(Integer)
    paired_ratio = Column(Float)
    window_start = Column(String(50))
    embedding_vector = Column(String(2048), nullable=False)
