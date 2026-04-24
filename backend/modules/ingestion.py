"""
Data ingestion module for PathPilot RAG System.
Handles loading, chunking, and preparing documents for embedding.
"""
import json
import logging
from typing import List, Dict, Any
from pathlib import Path
from config import config

logger = logging.getLogger(__name__)


class Document:
    """Represents a chunked document with metadata."""
    
    def __init__(self, text: str, metadata: Dict[str, Any]):
        self.text = text
        self.metadata = metadata
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "metadata": self.metadata
        }


class DataIngestion:
    """Handles data loading and chunking for RAG pipeline."""
    
    def __init__(self):
        self.data_dir = config.DATA_DIR
    
    def load_json(self, filename: str) -> Any:
        """Load JSON data file."""
        filepath = self.data_dir / filename
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded {filename} with {len(data) if isinstance(data, list) else 'object'} entries")
            return data
        except Exception as e:
            logger.error(f"Failed to load {filename}: {e}")
            raise
    
    def chunk_careers(self, careers: List[Dict]) -> List[Document]:
        """
        Chunk career data into semantic units.
        Each career becomes multiple chunks: overview, skills, roadmap phases.
        """
        documents = []
        
        for career in careers:
            # Career overview chunk
            overview_text = (
                f"Career: {career['title']}\n"
                f"Category: {career.get('category', 'General')}\n"
                f"Summary: {career.get('summary', '')}\n"
                f"Salary Range: {career.get('salary_range', 'N/A')}\n"
                f"Market Demand: {career.get('market_demand', 'N/A')}\n"
                f"Related Roles: {', '.join(career.get('related_roles', []))}"
            )
            documents.append(Document(
                text=overview_text,
                metadata={
                    "type": "career_overview",
                    "career_id": career['id'],
                    "title": career['title'],
                    "category": career.get('category', 'General'),
                    "chunk_type": "overview"
                }
            ))
            
            # Skills chunk
            skills = career.get('skills', {})
            all_skills = []
            for level in ['beginner', 'intermediate', 'advanced']:
                all_skills.extend(skills.get(level, []))
            
            if all_skills:
                skills_text = (
                    f"Career: {career['title']}\n"
                    f"Required Skills:\n"
                    f"Beginner: {', '.join(skills.get('beginner', []))}\n"
                    f"Intermediate: {', '.join(skills.get('intermediate', []))}\n"
                    f"Advanced: {', '.join(skills.get('advanced', []))}"
                )
                documents.append(Document(
                    text=skills_text,
                    metadata={
                        "type": "career_skills",
                        "career_id": career['id'],
                        "title": career['title'],
                        "category": career.get('category', 'General'),
                        "chunk_type": "skills",
                        "all_skills": all_skills
                    }
                ))
            
            # Roadmap phase chunks
            for phase in career.get('roadmap', []):
                phase_text = (
                    f"Career: {career['title']}\n"
                    f"Phase: {phase['phase']}\n"
                    f"Duration: {phase.get('duration', 'N/A')}\n"
                    f"Topics: {', '.join(phase.get('topics', []))}\n"
                    f"Resources: " + ", ".join([r['title'] for r in phase.get('resources', [])])
                )
                documents.append(Document(
                    text=phase_text,
                    metadata={
                        "type": "career_roadmap",
                        "career_id": career['id'],
                        "title": career['title'],
                        "category": career.get('category', 'General'),
                        "chunk_type": "roadmap",
                        "phase": phase['phase'],
                        "duration": phase.get('duration', 'N/A')
                    }
                ))
        
        logger.info(f"Chunked {len(careers)} careers into {len(documents)} documents")
        return documents
    
    def chunk_startups(self, startups: List[Dict]) -> List[Document]:
        """
        Chunk startup data into semantic units.
        Each startup framework becomes multiple chunks: overview, stages, metrics.
        """
        documents = []
        
        for startup in startups:
            # Overview chunk
            overview_text = (
                f"Startup Type: {startup['title']}\n"
                f"Category: {startup.get('category', 'General')}\n"
                f"Framework: {startup.get('framework', 'N/A')}\n"
                f"Description: {startup.get('description', '')}\n"
                f"Funding Options: {', '.join(startup.get('funding_options', []))}\n"
                f"Key Metrics: {', '.join(startup.get('key_metrics', []))}"
            )
            documents.append(Document(
                text=overview_text,
                metadata={
                    "type": "startup_overview",
                    "startup_id": startup['id'],
                    "title": startup['title'],
                    "category": startup.get('category', 'General'),
                    "chunk_type": "overview"
                }
            ))
            
            # Stage chunks
            for stage in startup.get('stages', []):
                stage_text = (
                    f"Startup Type: {startup['title']}\n"
                    f"Stage: {stage['name']}\n"
                    f"Duration: {stage.get('duration', 'N/A')}\n"
                    f"Steps:\n" + "\n".join([f"- {step}" for step in stage.get('steps', [])]) + "\n"
                    f"Common Pitfalls: {', '.join(stage.get('common_pitfalls', []))}\n"
                    f"Resources: " + ", ".join([r['title'] for r in stage.get('resources', [])])
                )
                documents.append(Document(
                    text=stage_text,
                    metadata={
                        "type": "startup_stage",
                        "startup_id": startup['id'],
                        "title": startup['title'],
                        "category": startup.get('category', 'General'),
                        "chunk_type": "stage",
                        "stage_name": stage['name'],
                        "duration": stage.get('duration', 'N/A')
                    }
                ))
            
            # Case studies chunks
            for case in startup.get('case_studies', []):
                case_text = (
                    f"Startup Type: {startup['title']}\n"
                    f"Case Study: {case['company']}\n"
                    f"Summary: {case.get('summary', '')}\n"
                    f"Key Learnings: {', '.join(case.get('key_learnings', []))}"
                )
                documents.append(Document(
                    text=case_text,
                    metadata={
                        "type": "startup_case_study",
                        "startup_id": startup['id'],
                        "title": startup['title'],
                        "category": startup.get('category', 'General'),
                        "chunk_type": "case_study",
                        "company": case['company']
                    }
                ))
        
        logger.info(f"Chunked {len(startups)} startups into {len(documents)} documents")
        return documents
    
    def chunk_financial_data(self, financial_data: Dict) -> List[Document]:
        """
        Chunk financial data into semantic units.
        Creates chunks for stocks, strategies, and frameworks.
        """
        documents = []
        
        # Stock chunks
        for stock in financial_data.get('stocks', []):
            stock_text = (
                f"Stock: {stock['name']} ({stock['symbol']})\n"
                f"Sector: {stock.get('sector', 'N/A')}\n"
                f"Current Price: ${stock.get('current_price', 'N/A')}\n"
                f"Market Cap: {stock.get('market_cap', 'N/A')}\n"
                f"P/E Ratio: {stock.get('pe_ratio', 'N/A')}\n"
                f"Dividend Yield: {stock.get('dividend_yield', 'N/A')}%\n"
                f"52-Week Range: ${stock.get('52_week_low', 'N/A')} - ${stock.get('52_week_high', 'N/A')}\n"
                f"Trend: {stock.get('trend', 'N/A')}\n"
                f"Key Metrics: Revenue Growth {stock.get('key_metrics', {}).get('revenue_growth', 'N/A')}, "
                f"Profit Margin {stock.get('key_metrics', {}).get('profit_margin', 'N/A')}\n"
                f"Analysis: {stock.get('analysis', '')}"
            )
            documents.append(Document(
                text=stock_text,
                metadata={
                    "type": "financial_stock",
                    "symbol": stock['symbol'],
                    "name": stock['name'],
                    "sector": stock.get('sector', 'N/A'),
                    "chunk_type": "stock"
                }
            ))
        
        # Investment strategy chunks
        for strategy in financial_data.get('investment_strategies', []):
            strategy_text = (
                f"Strategy: {strategy['name']}\n"
                f"Description: {strategy.get('description', '')}\n"
                f"Risk Level: {strategy.get('risk_level', 'N/A')}\n"
                f"Time Horizon: {strategy.get('time_horizon', 'N/A')}\n"
                f"Key Metrics: {', '.join(strategy.get('key_metrics', []))}\n"
                f"Pros: {', '.join(strategy.get('pros', []))}\n"
                f"Cons: {', '.join(strategy.get('cons', []))}"
            )
            documents.append(Document(
                text=strategy_text,
                metadata={
                    "type": "financial_strategy",
                    "strategy_name": strategy['name'],
                    "risk_level": strategy.get('risk_level', 'N/A'),
                    "chunk_type": "strategy"
                }
            ))
        
        # Market analysis framework chunks
        frameworks = financial_data.get('market_analysis_frameworks', {})
        for framework_name, framework_data in frameworks.items():
            framework_text = (
                f"Framework: {framework_name.replace('_', ' ').title()}\n"
                f"Description: {framework_data.get('description', '')}\n"
                f"Components: {', '.join(framework_data.get('components', []))}\n"
                f"Tools: {', '.join(framework_data.get('tools', []))}"
            )
            documents.append(Document(
                text=framework_text,
                metadata={
                    "type": "financial_framework",
                    "framework_name": framework_name,
                    "chunk_type": "framework"
                }
            ))
        
        logger.info(f"Chunked financial data into {len(documents)} documents")
        return documents
    
    def ingest_all(self) -> List[Document]:
        """Load and chunk all datasets."""
        all_documents = []
        
        try:
            # Load and chunk careers
            careers = self.load_json("careers.json")
            all_documents.extend(self.chunk_careers(careers))
        except Exception as e:
            logger.error(f"Error processing careers: {e}")
        
        try:
            # Load and chunk startups
            startups = self.load_json("startups.json")
            all_documents.extend(self.chunk_startups(startups))
        except Exception as e:
            logger.error(f"Error processing startups: {e}")
        
        try:
            # Load and chunk financial data
            financial_data = self.load_json("financial_data.json")
            all_documents.extend(self.chunk_financial_data(financial_data))
        except Exception as e:
            logger.error(f"Error processing financial data: {e}")
        
        logger.info(f"Total documents ingested: {len(all_documents)}")
        return all_documents
