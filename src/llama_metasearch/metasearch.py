# README.md
# Llama Metasearch

A sophisticated metasearch engine with adaptive engine selection, federated result aggregation, and bias detection.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11-blue)](https://www.python.org/)

## Features

- **Adaptive Engine Selection**: Uses reinforcement learning to select the best search providers for each query
- **Federated Result Aggregation**: Combines results from multiple search engines using Reciprocal Rank Fusion and other strategies
- **Cross-Engine Deduplication**: Identifies and removes duplicate results across different providers
- **Query Intent Classification**: Automatically classifies queries by intent to optimize search strategies
- **Bias Detection**: Identifies various types of bias in search results, including provider, commercial, and source bias
- **Dark Pattern Detection**: Detects and flags manipulative patterns in search results
- **Attribution Preservation**: Maintains proper attribution of results to their sources
- **Secure API Key Management**: Loads API keys securely from environment variables

## Installation

### Basic Installation

```bash
pip install llama-metasearch
```

### Full Installation (with ML features)

```bash
pip install llama-metasearch[full]
```

### Development Installation

```bash
pip install llama-metasearch[dev]
```

## Architecture

Llama Metasearch consists of several modular components:

1. **MetasearchOrchestrator**: The main entry point that coordinates all components
2. **AdaptiveEngineSelector**: Selects the most appropriate search engines for each query
3. **FederatedAggregator**: Combines results from multiple search engines
4. **CrossEngineDeduplicator**: Removes duplicate results
5. **QueryIntentClassifier**: Classifies the intent of search queries
6. **BiasDetector**: Detects various types of bias in search results
7. **Search Providers**: Interfaces with different search engines (Google, Bing, DuckDuckGo)

## Environment Variables

Configure your API keys using the following environment variables:

```
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CX=your_google_custom_search_id
BING_API_KEY=your_bing_api_key
```

You can create a `.env` file in your project directory and use `python-dotenv` to load them:

```python
from dotenv import load_dotenv

load_dotenv()
```

## Usage Examples

### Basic Usage

```python
import asyncio

from llama_metasearch import MetasearchOrchestrator, Query


async def main():
    # Initialize the orchestrator
    orchestrator = MetasearchOrchestrator()
    
    # Perform a search
    results, metadata = await orchestrator.search("adaptive search algorithms")
    
    # Print results
    for result in results:
        print(f"{result.title} - {result.url}")
        print(f"Snippet: {result.snippet}")
        print(f"Provider: {result.provider}, Rank: {result.rank}")
        print()
    
    # Print metadata
    print(f"Total search time: {metadata.total_search_time} ms")
    print(f"Engines used: {metadata.engines_used}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Advanced Usage with Custom Components

```python
import asyncio

from llama_metasearch import (AdaptiveEngineSelector, BiasDetector,
                              BingSearchProvider, CrossEngineDeduplicator,
                              DuckDuckGoSearchProvider, FederatedAggregator,
                              GoogleSearchProvider, MetasearchOrchestrator,
                              QueryIntentClassifier)


async def main():
    # Initialize providers
    google = GoogleSearchProvider()
    bing = BingSearchProvider()
    duckduckgo = DuckDuckGoSearchProvider()
    
    providers = {
        "Google": google,
        "Bing": bing,
        "DuckDuckGo": duckduckgo
    }
    
    # Initialize components with custom settings
    engine_selector = AdaptiveEngineSelector(
        available_providers=providers,
        use_rl=True,
        min_providers=1,
        max_providers=2
    )
    
    aggregator = FederatedAggregator(
        strategy="rrf",
        rrf_k=60,
        preserve_provider_diversity=True
    )
    
    deduplicator = CrossEngineDeduplicator(
        similarity_threshold=0.85,
        url_based=True,
        content_based=True,
        title_based=True
    )
    
    intent_classifier = QueryIntentClassifier(
        use_pretrained=True,
        use_heuristics=True
    )
    
    bias_detector = BiasDetector(
        use_shap=True,
        use_heuristics=True,
        bias_threshold=0.7,
    )
    
    # Initialize orchestrator with custom components
    orchestrator = MetasearchOrchestrator(
        providers=providers,
        engine_selector=engine_selector,
        aggregator=aggregator,
        deduplicator=deduplicator,
        intent_classifier=intent_classifier,
        bias_detector=bias_detector,
        default_num_results=10,
        preserve_attribution=True,
        detect_dark_patterns=True
    )
    
    # Perform a search
    results, metadata = await orchestrator.search(
        "best restaurants near me",
        num_results=5,
        parameters={"gl": "us", "location": "New York"}
    )
    
    # Print results
    for result in results:
        print(f"{result.title} - {result.url}")
        print(f"Snippet: {result.snippet}")
        print(f"Provider: {result.provider}, Rank: {result.rank}")
        if result.dark_pattern_flags:
            print(f"Dark Patterns Detected: {result.dark_pattern_flags}")
        print()
    
    # Print bias analysis
    if metadata.bias_analysis["any_bias_detected"]:
        print("Bias detected in search results:")
        for bias_type, bias_info in metadata.bias_analysis.items():
            if isinstance(bias_info, dict) and bias_info.get("detected", False):
                print(f"- {bias_type}: {bias_info.get('bias_score', 0)}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Using Different Aggregation Strategies

```python
import asyncio

from llama_metasearch import FederatedAggregator, MetasearchOrchestrator


async def main():
    # Initialize aggregator with interleaving strategy
    aggregator = FederatedAggregator(
        strategy="interleaving",
        interleaving_depth=3
    )
    
    # Initialize orchestrator with custom aggregator
    orchestrator = MetasearchOrchestrator(
        aggregator=aggregator
    )
    
    # Perform a search
    results, metadata = await orchestrator.search("renewable energy sources")
    
    # Print results
    for result in results:
        print(f"{result.title} - {result.provider}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Custom Result Scoring Function

```python
import asyncio

from llama_metasearch import (FederatedAggregator, MetasearchOrchestrator,
                              SearchResult)


# Define custom scoring function
def score_by_domain_authority(result: SearchResult) -> float:
    """Score results based on domain authority and freshness."""
    # Example logic - in practice, you might use a real domain authority API
    domain_scores = {
        "wikipedia.org": 0.9,
        "github.com": 0.8,
        "nytimes.com": 0.85,
        "medium.com": 0.7
    }
    
    # Extract domain from URL
    from urllib.parse import urlparse
    domain = urlparse(result.url).netloc
    
    # Get base domain
    base_domain = ".".join(domain.split(".")[-2:])
    
    # Calculate score
    base_score = domain_scores.get(base_domain, 0.5)
    
    # Consider recency if available in metadata
    if "date_published" in result.metadata:
        import datetime
        pub_date = datetime.datetime.fromisoformat(result.metadata["date_published"])
        days_old = (datetime.datetime.now() - pub_date).days
        recency_factor = max(0.5, 1.0 - (days_old / 365))
        return base_score * recency_factor
    
    return base_score

async def main():
    # Initialize aggregator with custom scoring
    aggregator = FederatedAggregator(
        strategy="custom",
        custom_scoring_function=score_by_domain_authority
    )
    
    # Initialize orchestrator
    orchestrator = MetasearchOrchestrator(
        aggregator=aggregator
    )
    
    # Perform search
    results, _ = await orchestrator.search("latest research machine learning")
    
    # Print results
    for result in results:
        print(f"{result.title} - {result.url}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

# Test global
_, _, locality, locality_conf = self.classifier._apply_heuristics(
    "global warming impact worldwide"
)

self.assertEqual(locality, QueryLocality.GLOBAL)
self.assertGreaterEqual(locality_conf, 0.8)

def test_classify_with_heuristics(self):
    """Test classification with heuristics only."""
    # Configure classifier to use only heuristics
    classifier = QueryIntentClassifier(
        use_pretrained=False,
        use_heuristics=True,
        heuristics_confidence_threshold=0.7
    )
    
    # Create a query with obvious intent
    query = Query(text="restaurants near me open now")
    classified = classifier.classify(query)
    
    # Should classify as LOCAL intent
    self.assertEqual(classified.intent, QueryIntent.LOCAL)
    # Should classify as LOCAL locality
    self.assertEqual(classified.locality, QueryLocality.LOCAL)

def test_classify_without_heuristics(self):
    """Test classification without heuristics."""
    # Configure classifier to use neither heuristics nor ML model
    classifier = QueryIntentClassifier(
        use_pretrained=False,
        use_heuristics=False
    )
    
    # Create a query
    query = Query(text="some ambiguous query")
    classified = classifier.classify(query)
    
    # Should default to INFORMATIONAL intent
    self.assertEqual(classified.intent, QueryIntent.INFORMATIONAL)
    # Should default to GLOBAL locality
    self.assertEqual(classified.locality, QueryLocality.GLOBAL)

@patch('llama_metasearch.intent_classifier.HAVE_TRANSFORMERS', True)
@patch('llama_metasearch.intent_classifier.AutoTokenizer')
@patch('llama_metasearch.intent_classifier.AutoModelForSequenceClassification')
@patch('llama_metasearch.intent_classifier.torch')
def test_model_classification(self, mock_torch, mock_model_class, mock_tokenizer_class):
    """Test classification using a ML model."""
    # Set up mocks
    mock_tokenizer = MagicMock()
    mock_tokenizer_class.from_pretrained.return_value = mock_tokenizer
    
    mock_model = MagicMock()
    mock_model_class.from_pretrained.return_value = mock_model
    
    mock_outputs = MagicMock()
    mock_logits = MagicMock()
    mock_outputs.logits = mock_logits
    mock_model.return_value = mock_outputs
    
    mock_probs = MagicMock()
    mock_torch.nn.functional.softmax.return_value = [mock_probs]
    
    # Configure mock to return specific intent
    mock_probs.__getitem__.return_value.item.return_value = 0.9
    mock_torch.argmax.return_value.item.return_value = 0  # 0 maps to INFORMATIONAL
    
    # Create classifier with mock model
    classifier = QueryIntentClassifier(
        use_pretrained=True,
        use_heuristics=False
    )
    classifier.intent_model = mock_model
    classifier.intent_tokenizer = mock_tokenizer
    classifier.locality_model = mock_model
    classifier.locality_tokenizer = mock_tokenizer
    
    # Classify with model
    intent, intent_conf, locality, locality_conf = classifier._model_classification("test query")
    
    # Verify results
    self.assertEqual(intent, QueryIntent.INFORMATIONAL)
    self.assertAlmostEqual(intent_conf, 0.9)
    
    # Verify model was called
    mock_tokenizer.assert_called()
    mock_model.assert_called()

def test_cache_functionality(self):
    """Test classification cache functionality."""
    # Create classifier with cache
    classifier = QueryIntentClassifier(
        use_pretrained=False,
        use_heuristics=True,
        cache_size=10
    )
    
    # Classify a query
    query_text = "restaurants near me"
    query = Query(text=query_text)
    classifier.classify(query)
    
    # Verify query is in cache
    self.assertIn(query_text.lower().strip(), classifier.cache)
    
    # Spoof the heuristics to return different results
    original_heuristics = classifier._apply_heuristics
    
    def mock_heuristics(text):
        return (QueryIntent.VISUAL, 0.9, QueryLocality.GLOBAL, 0.9)
    
    classifier._apply_heuristics = mock_heuristics
    
    # Classify same query again
    query = Query(text=query_text)
    classified = classifier.classify(query)
    
    # Should use cached result, not the spoofed heuristics
    self.assertEqual(classified.intent, QueryIntent.LOCAL)
    self.assertEqual(classified.locality, QueryLocality.LOCAL)
    
    # Restore original heuristics
    classifier._apply_heuristics = original_heuristics

def test_cache_size_limit(self):
    """Test cache size limiting."""
    # Create classifier with small cache
    cache_size = 2
    classifier = QueryIntentClassifier(
        use_pretrained=False,
        use_heuristics=True,
        cache_size=cache_size
    )
    
    # Fill cache beyond limit
    for i in range(cache_size + 2):
        query = Query(text=f"query {i}")
        classifier.classify(query)
    
    # Cache should not exceed size limit
    self.assertLessEqual(len(classifier.cache), cache_size)

def test_save_load_cache(self):
    """Test saving and loading the classification cache."""
    # Create classifier
    classifier = QueryIntentClassifier(
        use_pretrained=False,
        use_heuristics=True
    )
    
    # Add entries to cache
    classifier.cache = {
        "query1": (QueryIntent.INFORMATIONAL, 0.9, QueryLocality.GLOBAL, 0.9),
        "query2": (QueryIntent.NAVIGATIONAL, 0.8, QueryLocality.LOCAL, 0.8)
    }
    
    # Create temp file
    with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as tmp_file:
        cache_path = tmp_file.name
    
    try:
        # Save cache
        classifier.save_cache(cache_path)
        
        # Create new classifier
        new_classifier = QueryIntentClassifier(
            use_pretrained=False,
            use_heuristics=True
        )
        
        # Load cache
        new_classifier.load_cache(cache_path)
        
        # Verify cache was loaded
        self.assertEqual(len(new_classifier.cache), 2)
        self.assertIn("query1", new_classifier.cache)
        self.assertIn("query2", new_classifier.cache)
        
        # Verify cache entries
        self.assertEqual(new_classifier.cache["query1"][0], QueryIntent.INFORMATIONAL)
        self.assertEqual(new_classifier.cache["query2"][0], QueryIntent.NAVIGATIONAL)
    finally:
        # Clean up
        if os.path.exists(cache_path):
            os.remove(cache_path)

def test_load_cache_with_invalid_data(self):
    """Test loading cache with invalid data."""
    # Create classifier
    classifier = QueryIntentClassifier(
        use_pretrained=False,
        use_heuristics=True
    )
    
    # Create temp file with invalid data
    with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as tmp_file:
        cache_path = tmp_file.name
        # Write invalid pickle data
        tmp_file.write(b'invalid data')
    
    try:
        # Try to load invalid cache
        classifier.load_cache(cache_path)
        
        # Cache should be empty
        self.assertEqual(len(classifier.cache), 0)
    finally:
        # Clean up
        if os.path.exists(cache_path):
            os.remove(cache_path)

# llama_metasearch/tests/test_bias_detector.py
"""Tests for the BiasDetector class."""

import unittest
from unittest.mock import MagicMock, patch

from ..bias_detector import BiasDetector
from ..models.result import SearchResult


class TestBiasDetector(unittest.TestCase):
    """Test cases for the BiasDetector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create test results
        self.results = [
            # Results from Google
            SearchResult(
                title="Buy the best product now",
                url="https://store.example.com/product",
                snippet="Limited time offer! Buy now before it's gone. Best prices guaranteed.",
                provider="Google",
                rank=1,
                is_ad=True
            ),
            SearchResult(
                title="Example.com - Official Website",
                url="https://example.com",
                snippet="Example Corporation's official website. Learn about our products and services.",
                provider="Google",
                rank=2
            ),
            SearchResult(
                title="Example Review - Independent Analysis",
                url="https://reviews.example.org/example",
                snippet="Our independent review of Example's products. Pros and cons analyzed.",
                provider="Google",
                rank=3
            ),
            
            # Results from Bing - add provider bias
            SearchResult(
                title="Example.com - Home",
                url="https://example.com",
                snippet="Welcome to Example.com, the home of the best products.",
                provider="Bing",
                rank=1
            ),
            SearchResult(
                title="Buy Example Products - Official Store",
                url="https://store.example.com",
                snippet="Shop all Example products. Free shipping on orders over $50!",
                provider="Bing",
                rank=2
            ),
            
            # Results from Domain A - add source bias
            SearchResult(
                title="Example Product Review",
                url="https://blog.biased-domain.com/review1",
                snippet="Our review of the Example product. The best in its class!",
                provider="DuckDuckGo",
                rank=1
            ),
            SearchResult(
                title="Why Example Products Are Superior",
                url="https://blog.biased-domain.com/article1",
                snippet="Analysis shows Example products outperform competitors in every metric.",
                provider="DuckDuckGo",
                rank=2
            ),
            SearchResult(
                title="Example vs Competitor - No Contest",
                url="https://blog.biased-domain.com/comparison",
                snippet="Comparing Example to its competitors. Example wins hands down!",
                provider="DuckDuckGo",
                rank=3
            )
        ]
        
        # Initialize detector
        self.detector = BiasDetector(
            use_shap=False,  # Disable SHAP for basic tests
            use_heuristics=True,
            bias_threshold=0.7
        )
    
    def test_detect_provider_bias(self):
        """Test detecting provider bias."""
        # Create results with provider bias
        biased_results = [
            SearchResult(
                title=f"Result {i}",
                url=f"https://example.com/{i}",
                snippet=f"Snippet {i}",
                provider="DominantProvider",
                rank=i
            )
            for i in range(1, 8)
        ]
        
        # Add a few results from other providers
        biased_results.extend([
            SearchResult(
                title="Other Result 1",
                url="https://other.com/1",
                snippet="Other snippet 1",
                provider="OtherProvider1",
                rank=1
            ),
            SearchResult(
                title="Other Result 2",
                url="https://other.com/2",
                snippet="Other snippet 2",
                provider="OtherProvider2",
                rank=1
            )
        ])
        
        # Detect bias
        bias_results = self.detector._detect_provider_bias(biased_results)
        
        # Should detect bias
        self.assertTrue(bias_results["detected"])
        self.assertGreater(bias_results["bias_score"], self.detector.bias_threshold)
        self.assertEqual(bias_results["dominant_provider"], "DominantProvider")
        
        # Test with balanced results
        balanced_results = []
        for provider in ["Provider1", "Provider2", "Provider3"]:
            for i in range(1, 4):
                balanced_results.append(
                    SearchResult(
                        title=f"{provider} Result {i}",
                        url=f"https://{provider.lower()}.com/{i}",
                        snippet=f"{provider} snippet {i}",
                        provider=provider,
                        rank=i
                    )
                )
        
        # Detect bias
        bias_results = self.detector._detect_provider_bias(balanced_results)
        
        # Should not detect bias
        self.assertFalse(bias_results["detected"])
        self.assertLess(bias_results["bias_score"], self.detector.bias_threshold)
        self.assertIsNone(bias_results["dominant_provider"])
    
    def test_detect_commercial_bias(self):
        """Test detecting commercial bias."""
        # Create results with commercial bias
        commercial_results = [
            SearchResult(
                title="Buy Product Now",
                url="https://store.com/product",
                snippet="Great discount! Limited time offer. Buy now!",
                provider="Provider1",
                rank=1,
                is_ad=True
            ),
            SearchResult(
                title="Shop Online - Best Prices",
                url="https://shop.com",
                snippet="Shop our selection of products. Free shipping on orders over $50!",
                provider="Provider2",
                rank=1
            ),
            SearchResult(
                title="Discount Coupons for Product",
                url="https://coupons.com/product",
                snippet="Get the best discount coupons for your favorite products.",
                provider="Provider3",
                rank=1
            ),
            SearchResult(
                title="Product Information",
                url="https://info.com/product",
                snippet="Learn about the product features and specifications.",
                provider="Provider4",
                rank=1
            )
        ]
        
        # Detect bias
        bias_results = self.detector._detect_commercial_bias(commercial_results)
        
        # Should detect commercial bias
        self.assertTrue(bias_results["detected"])
        self.assertGreater(bias_results["bias_score"], self.detector.bias_threshold)
        self.assertGreaterEqual(bias_results["commercial_result_count"], 3)
        
        # Test with non-commercial results
        non_commercial_results = [
            SearchResult(
                title="Product Information",
                url="https://info.com/product",
                snippet="Learn about the product features and specifications.",
                provider="Provider1",
                rank=1
            ),
            SearchResult(
                title="Product Review",
                url="https://reviews.com/product",
                snippet="Independent review of the product.",
                provider="Provider2",
                rank=1
            ),
            SearchResult(
                title="Product History",
                url="https://history.com/product",
                snippet="The history of the product development.",
                provider="Provider3",
                rank=1
            )
        ]
        
        # Detect bias
        bias_results = self.detector._detect_commercial_bias(non_commercial_results)
        
        # Should not detect commercial bias
        self.assertFalse(bias_results["detected"])
        self.assertLess(bias_results["bias_score"], self.detector.bias_threshold)
    
    def test_detect_source_bias(self):
        """Test detecting source (domain) bias."""
        # Create results with source bias
        source_biased_results = [
            SearchResult(
                title=f"Result {i}",
                url=f"https://biased-domain.com/page{i}",
                snippet=f"Snippet {i}",
                provider="Provider1",
                rank=i
            )
            for i in range(1, 8)
        ]
        
        # Add a few results from other domains
        source_biased_results.extend([
            SearchResult(
                title="Other Result 1",
                url="https://other1.com/1",
                snippet="Other snippet 1",
                provider="Provider2",
                rank=1
            ),
            SearchResult(
                title="Other Result 2",
                url="https://other2.com/2",
                snippet="Other snippet 2",
                provider="Provider3",
                rank=1
            )
        ])
        
        # Detect bias
        bias_results = self.detector._detect_source_bias(source_biased_results)
        
        # Should detect source bias
        self.assertTrue(bias_results["detected"])
        self.assertGreater(bias_results["bias_score"], self.detector.bias_threshold)
        self.assertEqual(bias_results["top_domains"][0][0], "biased-domain.com")
        
        # Test with diverse sources
        diverse_results = []
        for i in range(1, 10):
            diverse_results.append(
                SearchResult(
                    title=f"Result {i}",
                    url=f"https://domain{i}.com/page",
                    snippet=f"Snippet {i}",
                    provider=f"Provider{(i % 3) + 1}",
                    rank=i
                )
            )
        
        # Detect bias
        bias_results = self.detector._detect_source_bias(diverse_results)
        
        # Should not detect source bias
        self.assertFalse(bias_results["detected"])
        self.assertLess(bias_results["bias_score"], self.detector.bias_threshold)
    
    def test_detect_dark_patterns(self):
        """Test detecting dark patterns."""
        # Create results with dark patterns
        dark_pattern_results = [
            SearchResult(
                title="Limited Time Offer - Act Now!",
                url="https://store.com/offer",
                snippet="Only 2 left in stock! Order now before they're gone!",
                provider="Provider1",
                rank=1
            ),
            SearchResult(
                title="Exclusive Deal - Today Only",
                url="https://shop.com/deal",
                snippet="Flash sale ending soon. 90% of customers recommend this product!",
                provider="Provider2",
                rank=1
            ),
            SearchResult(
                title="Product Information",
                url="https://info.com/product",
                snippet="Learn about the product features and specifications.",
                provider="Provider3",
                rank=1
            )
        ]
        
        # Detect dark patterns
        pattern_results = self.detector._detect_dark_patterns(dark_pattern_results)
        
        # Should detect dark patterns
        self.assertTrue(pattern_results["detected"])
        self.assertGreater(pattern_results["pattern_count"], 0)
        self.assertGreaterEqual(len(pattern_results["pattern_results"]), 2)
        
        # Check that patterns were added to result flags
        self.assertGreater(len(dark_pattern_results[0].dark_pattern_flags), 0)
        self.assertGreater(len(dark_pattern_results[1].dark_pattern_flags), 0)
    
    @patch('llama_metasearch.bias_detector.HAVE_SHAP', True)
    def test_analyze_bias_with_shap(self):
        """Test SHAP-based bias analysis."""
        # This is a simplified test that mocks SHAP functionality
        
        # Create detector with SHAP
        detector = BiasDetector(
            use_shap=True,
            use_heuristics=True
        )
        
        # Mock SHAP components
        detector.vectorizer = MagicMock()
        detector.model = MagicMock()
        detector.shap_explainer = MagicMock()
        
        # Mock feature names
        detector.vectorizer.get_feature_names_out.return_value = [
            "product", "buy", "discount", "review", "information"
        ]
        
        # Mock SHAP values
        mock_shap_values = MagicMock()
        mock_shap_values.values = [
            [0.5, 0.8, 0.7, 0.3, 0.2]  # Values for each feature
        ]
        detector.shap_explainer.return_value = mock_shap_values
        
        # Run analysis
        shap_results = detector._analyze_bias_with_shap(self.results)
        
        # Verify SHAP was used
        self.assertTrue(shap_results["used_shap"])
        
        # Verify top features were extracted
        self.assertGreaterEqual(len(shap_results["top_influential_features"]), 1)
    
    def test_analyze_comprehensive(self):
        """Test comprehensive bias analysis."""
        # Run full analysis on test results
        analysis = self.detector.analyze(self.results)
        
        # Verify structure
        self.assertIn("any_bias_detected", analysis)
        self.assertIn("provider_bias", analysis)
        self.assertIn("commercial_bias", analysis)
        self.assertIn("source_bias", analysis)
        self.assertIn("dark_patterns", analysis)
        self.assertIn("attribution", analysis)
        
        # Check if our test data triggered any bias detection
        bias_detected = any([
            analysis["provider_bias"].get("detected", False),
            analysis["commercial_bias"].get("detected", False),
            analysis["source_bias"].get("detected", False),
            analysis["dark_patterns"].get("detected", False)
        ])
        
        self.assertEqual(analysis["any_bias_detected"], bias_detected)

# pyproject.toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "llama_metasearch"
version = "0.1.0"
description = "A sophisticated metasearch engine with adaptive engine selection, federated result aggregation, and bias detection"
readme = "README.md"
authors = [
    {name = "Llama Metasearch Team"}
]
license = {text = "MIT"}
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
requires-python = ">=3.8"
dependencies = [
    "aiohttp>=3.8.0",
    "python-dotenv>=0.19.0",
    "tqdm>=4.62.0",
    "numpy>=1.20.0",
    "urllib3>=1.26.0",
]

[project.optional-dependencies]
full = [
    "transformers>=4.20.0",
    "torch>=1.9.0",
    "sentence-transformers>=2.2.0",
    "scikit-learn>=1.0.0",
    "shap>=0.40.0",
]
dev = [
    "pytest>=6.0",
    "pytest-asyncio>=0.16.0",
    "black>=22.0.0",
    "isort>=5.10.0",
    "flake8>=4.0.0",
    "mypy>=0.910",
    "coverage>=6.0",
    "pytest-cov>=2.12.0",
]

[project.urls]
"Homepage" = "https://github.com/username/llama-metasearch"
"Bug Tracker" = "https://github.com/username/llama-metasearch/issues"

[tool.setuptools]
packages = ["llama_metasearch"]

[tool.black]
line-length = 88
target-version = ["py38"]

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true

[[tool.mypy.overrides]]
module = [
    "torch.*",
    "transformers.*",
    "sentence_transformers.*",
    "shap.*",
    "sklearn.*",
    "tqdm.*",
]
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["llama_metasearch/tests"]
python_files = "test_*.py"
asyncio_mode = "auto"

# requirements.txt
aiohttp>=3.8.0
python-dotenv>=0.19.0
tqdm>=4.62.0
numpy>=1.20.0
urllib3>=1.26.0

# requirements-dev.txt
transformers>=4.20.0
torch>=1.9.0
sentence-transformers>=2.2.0
scikit-learn>=1.0.0
shap>=0.40.0
pytest>=6.0
pytest-asyncio>=0.16.0
black>=22.0.0
isort>=5.10.0
flake8>=4.0.0
mypy>=0.910
coverage>=6.0
pytest-cov>=2.12.0

# File structure for the package:
# llama_metasearch/
# ├── __init__.py
# ├── orchestrator.py
# ├── engine_selector.py
# ├── aggregator.py
# ├── deduplicator.py
# ├── intent_classifier.py
# ├── bias_detector.py
# ├── providers/
# │   ├── __init__.py
# │   ├── base.py
# │   ├── google.py
# │   ├── bing.py
# │   └── duckduckgo.py
# ├── utils/
# │   ├── __init__.py
# │   ├── config.py
# │   ├── logging.py
# │   └── metrics.py
# ├── models/
# │   ├── __init__.py
# │   ├── result.py
# │   ├── query.py
# │   └── metadata.py
# ├── tests/
# │   ├── __init__.py
# │   ├── test_orchestrator.py
# │   ├── test_engine_selector.py
# │   ├── test_aggregator.py
# │   ├── test_deduplicator.py
# │   ├── test_intent_classifier.py
# │   └── test_bias_detector.py
# ├── pyproject.toml
# ├── requirements.txt
# ├── requirements-dev.txt
# └── README.md

# Let's implement each file one by one:

# llama_metasearch/__init__.py
"""
Llama Metasearch: A sophisticated metasearch package.

This package provides a comprehensive metasearch solution with adaptive engine selection,
federated result aggregation, cross-engine deduplication, query intent classification, 
and bias detection capabilities.
"""

__version__ = "0.1.0"

from .orchestrator import MetasearchOrchestrator
from .models.result import SearchResult
from .models.query import Query

__all__ = ["MetasearchOrchestrator", "SearchResult", "Query"]

# llama_metasearch/models/result.py
"""Models for search results and related data structures."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
import hashlib
import json


@dataclass
class SearchResult:
    """
    Represents a single search result from any search engine.
    
    Attributes:
        title: The title of the search result.
        url: The URL of the search result.
        snippet: A text snippet or description of the search result.
        provider: The search provider that returned this result.
        rank: The original rank position from the provider.
        timestamp: When the result was retrieved.
        metadata: Additional provider-specific metadata.
        content_type: The type of content (webpage, image, video, etc.).
        is_ad: Whether the result is marked as an advertisement.
        cached_url: URL to a cached version of the page if available.
        attribution: Attribution information for proper sourcing.
        dark_pattern_flags: Set of detected dark patterns if any.
    """
    
    title: str
    url: str
    snippet: str
    provider: str
    rank: int
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    content_type: str = "webpage"
    is_ad: bool = False
    cached_url: Optional[str] = None
    attribution: Optional[Dict[str, str]] = None
    dark_pattern_flags: Set[str] = field(default_factory=set)
    
    @property
    def result_id(self) -> str:
        """
        Generate a unique identifier for this search result.
        
        Returns:
            A hash string uniquely identifying this result.
        """
        key_data = f"{self.url}|{self.title}|{self.provider}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the search result to a dictionary.
        
        Returns:
            Dict representation of the search result.
        """
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "provider": self.provider,
            "rank": self.rank,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "content_type": self.content_type,
            "is_ad": self.is_ad,
            "cached_url": self.cached_url,
            "attribution": self.attribution,
            "dark_pattern_flags": list(self.dark_pattern_flags),
            "result_id": self.result_id
        }
    
    def to_json(self) -> str:
        """
        Convert the search result to a JSON string.
        
        Returns:
            JSON representation of the search result.
        """
        result_dict = self.to_dict()
        return json.dumps(result_dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SearchResult':
        """
        Create a SearchResult instance from a dictionary.
        
        Args:
            data: Dictionary with search result data.
            
        Returns:
            A new SearchResult instance.
        """
        # Handle timestamp conversion
        if "timestamp" in data and isinstance(data["timestamp"], str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
            
        # Handle dark pattern flags conversion
        if "dark_pattern_flags" in data and isinstance(data["dark_pattern_flags"], list):
            data["dark_pattern_flags"] = set(data["dark_pattern_flags"])
            
        return cls(**{k: v for k, v in data.items() if k != "result_id"})

# llama_metasearch/models/query.py
"""Models for search queries and related data structures."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import time
import uuid


class QueryIntent(Enum):
    """Enumeration of possible query intents."""
    
    INFORMATIONAL = "informational"
    NAVIGATIONAL = "navigational"
    TRANSACTIONAL = "transactional"
    COMMERCIAL = "commercial"
    LOCAL = "local"
    VISUAL = "visual"
    NEWS = "news"
    UNDEFINED = "undefined"


class QueryLocality(Enum):
    """Enumeration of possible query locality types."""
    
    GLOBAL = "global"
    LOCAL = "local"
    REGIONAL = "regional"
    NATIONAL = "national"
    UNDEFINED = "undefined"


@dataclass
class Query:
    """
    Represents a search query with its associated metadata.
    
    Attributes:
        text: The raw query text.
        intent: The classified intent of the query.
        locality: The locality type of the query.
        language: The language of the query.
        query_id: A unique identifier for the query.
        timestamp: When the query was created.
        processed_text: Query text after preprocessing.
        parameters: Additional query parameters.
        context: Contextual information for the query.
    """
    
    text: str
    intent: QueryIntent = QueryIntent.UNDEFINED
    locality: QueryLocality = QueryLocality.UNDEFINED
    language: str = "en"
    query_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    processed_text: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize processed_text if not provided."""
        if self.processed_text is None:
            self.processed_text = self.text
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the query to a dictionary.
        
        Returns:
            Dict representation of the query.
        """
        return {
            "text": self.text,
            "intent": self.intent.value,
            "locality": self.locality.value,
            "language": self.language,
            "query_id": self.query_id,
            "timestamp": self.timestamp,
            "processed_text": self.processed_text,
            "parameters": self.parameters,
            "context": self.context
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Query':
        """
        Create a Query instance from a dictionary.
        
        Args:
            data: Dictionary with query data.
            
        Returns:
            A new Query instance.
        """
        # Handle enum conversions
        if "intent" in data and isinstance(data["intent"], str):
            data["intent"] = QueryIntent(data["intent"])
            
        if "locality" in data and isinstance(data["locality"], str):
            data["locality"] = QueryLocality(data["locality"])
            
        return cls(**data)

# llama_metasearch/models/metadata.py
"""Models for metadata associated with search operations."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class SearchMetadata:
    """
    Metadata associated with a search operation.
    
    Attributes:
        query_processing_time: Time taken to process the query in milliseconds.
        engine_selection_time: Time taken to select engines in milliseconds.
        total_search_time: Total time taken for the search in milliseconds.
        engines_used: List of search engines used.
        result_counts: Count of results from each engine.
        aggregation_strategy: Strategy used for result aggregation.
        deduplication_stats: Statistics about deduplication.
        bias_analysis: Results of bias detection.
        timestamp: When the search was performed.
    """
    
    query_processing_time: float = 0.0
    engine_selection_time: float = 0.0
    total_search_time: float = 0.0
    engines_used: List[str] = field(default_factory=list)
    result_counts: Dict[str, int] = field(default_factory=dict)
    aggregation_strategy: str = "default"
    deduplication_stats: Dict[str, Any] = field(default_factory=dict)
    bias_analysis: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the metadata to a dictionary.
        
        Returns:
            Dict representation of the metadata.
        """
        return {
            "query_processing_time": self.query_processing_time,
            "engine_selection_time": self.engine_selection_time,
            "total_search_time": self.total_search_time,
            "engines_used": self.engines_used,
            "result_counts": self.result_counts,
            "aggregation_strategy": self.aggregation_strategy,
            "deduplication_stats": self.deduplication_stats,
            "bias_analysis": self.bias_analysis,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SearchMetadata':
        """
        Create a SearchMetadata instance from a dictionary.
        
        Args:
            data: Dictionary with metadata.
            
        Returns:
            A new SearchMetadata instance.
        """
        # Handle timestamp conversion
        if "timestamp" in data and isinstance(data["timestamp"], str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
            
        return cls(**data)

# llama_metasearch/providers/base.py
"""Base classes for search providers."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import time
import logging
from ..models.result import SearchResult
from ..models.query import Query

logger = logging.getLogger(__name__)


class SearchProvider(ABC):
    """
    Abstract base class for all search providers.
    
    This class defines the interface that all search providers must implement.
    """
    
    def __init__(self, name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize a search provider.
        
        Args:
            name: Name of the search provider.
            api_key: API key for the search provider.
            **kwargs: Additional provider-specific parameters.
        """
        self.name = name
        self.api_key = api_key
        self.kwargs = kwargs
        self.last_request_time = 0.0
        self._request_count = 0
        
        # Rate limiting parameters
        self.rate_limit_requests = kwargs.get("rate_limit_requests", 10)
        self.rate_limit_period = kwargs.get("rate_limit_period", 1.0)
    
    @abstractmethod
    async def search(self, query: Query, num_results: int = 10) -> List[SearchResult]:
        """
        Perform a search with the given query.
        
        Args:
            query: The search query.
            num_results: Maximum number of results to return.
            
        Returns:
            A list of search results.
        """
        pass
    
    @abstractmethod
    def validate_api_key(self) -> bool:
        """
        Validate the provided API key.
        
        Returns:
            True if the API key is valid, False otherwise.
        """
        pass
    
    def wait_for_rate_limit(self):
        """
        Wait if necessary to respect rate limits.
        """
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.rate_limit_period:
            # If we've made too many requests in the period, wait
            if self._request_count >= self.rate_limit_requests:
                wait_time = self.rate_limit_period - time_since_last_request
                logger.debug(f"Rate limiting {self.name}, waiting {wait_time:.2f}s")
                time.sleep(wait_time)
                self._request_count = 0
        else:
            # Reset counter if period has passed
            self._request_count = 0
        
        self._request_count += 1
        self.last_request_time = time.time()
    
    def get_provider_info(self) -> Dict[str, Any]:
        """
        Get information about this provider.
        
        Returns:
            A dictionary with provider information.
        """
        return {
            "name": self.name,
            "has_api_key": self.api_key is not None,
            "rate_limit_requests": self.rate_limit_requests,
            "rate_limit_period": self.rate_limit_period
        }
    
    def format_result(self, raw_result: Dict[str, Any], rank: int, query: Query) -> SearchResult:
        """
        Format a raw result from the search API into a SearchResult object.
        
        Args:
            raw_result: Raw result from the API.
            rank: Rank of the result.
            query: Original query.
            
        Returns:
            A formatted SearchResult.
        """
        # This is a base implementation that should be overridden by subclasses
        return SearchResult(
            title=raw_result.get("title", "Untitled"),
            url=raw_result.get("url", ""),
            snippet=raw_result.get("snippet", ""),
            provider=self.name,
            rank=rank,
            metadata={"raw": raw_result, "query_text": query.text}
        )

# llama_metasearch/providers/google.py
"""Google search provider implementation."""

import os
import json
import logging
import aiohttp
from typing import List, Dict, Any, Optional
from urllib.parse import urlencode

from .base import SearchProvider
from ..models.result import SearchResult
from ..models.query import Query

logger = logging.getLogger(__name__)


class GoogleSearchProvider(SearchProvider):
    """
    Google search provider using the Google Custom Search JSON API.
    
    This class implements the SearchProvider interface for Google Custom Search.
    """
    
    BASE_URL = "https://www.googleapis.com/customsearch/v1"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        cx: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the Google search provider.
        
        Args:
            api_key: Google API key. If None, will try to load from GOOGLE_API_KEY env var.
            cx: Google Custom Search Engine ID. If None, will try to load from GOOGLE_CX env var.
            **kwargs: Additional parameters to pass to the search API.
        """
        api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        cx = cx or os.environ.get("GOOGLE_CX")
        
        if not api_key:
            logger.warning("No Google API key provided. Searches will fail.")
        
        if not cx:
            logger.warning("No Google Custom Search Engine ID provided. Searches will fail.")
        
        super().__init__(name="Google", api_key=api_key, **kwargs)
        self.cx = cx
    
    async def search(self, query: Query, num_results: int = 10) -> List[SearchResult]:
        """
        Perform a Google search with the given query.
        
        Args:
            query: The search query.
            num_results: Maximum number of results to return.
            
        Returns:
            A list of search results.
        """
        if not self.api_key or not self.cx:
            logger.error("Google search failed: Missing API key or Custom Search Engine ID")
            return []
        
        self.wait_for_rate_limit()
        
        params = {
            "key": self.api_key,
            "cx": self.cx,
            "q": query.processed_text,
            "num": min(num_results, 10)  # Google API max is 10 per request
        }
        
        # Add optional parameters
        if "gl" in query.parameters:  # Country code
            params["gl"] = query.parameters["gl"]
            
        if "lr" in query.parameters:  # Language restriction
            params["lr"] = query.parameters["lr"]
            
        if "safe" in query.parameters:  # Safe search
            params["safe"] = query.parameters["safe"]
        
        try:
            async with aiohttp.ClientSession() as session:
                results = []
                
                # Handle pagination if num_results > 10
                for start_index in range(1, num_results + 1, 10):
                    if start_index > 1:
                        params["start"] = start_index
                    
                    url = f"{self.BASE_URL}?{urlencode(params)}"
                    logger.debug(f"Google search URL: {url}")
                    
                    async with session.get(url) as response:
                        if response.status != 200:
                            response_text = await response.text()
                            logger.error(f"Google search failed: {response.status} - {response_text}")
                            break
                        
                        data = await response.json()
                        
                        if "items" not in data:
                            logger.warning("No results found in Google response")
                            break
                        
                        # Process results
                        for i, item in enumerate(data["items"], start=start_index):
                            result = self.format_result(item, i, query)
                            results.append(result)
                            
                            if len(results) >= num_results:
                                break
                    
                    if len(results) >= num_results:
                        break
                
                return results
        
        except Exception as e:
            logger.exception(f"Error during Google search: {e}")
            return []
    
    def validate_api_key(self) -> bool:
        """
        Validate the provided Google API key.
        
        Returns:
            True if the API key is valid, False otherwise.
        """
        return self.api_key is not None and self.cx is not None
    
    def format_result(self, raw_result: Dict[str, Any], rank: int, query: Query) -> SearchResult:
        """
        Format a raw Google result into a SearchResult object.
        
        Args:
            raw_result: Raw result from the Google API.
            rank: Rank of the result.
            query: Original query.
            
        Returns:
            A formatted SearchResult.
        """
        title = raw_result.get("title", "Untitled")
        url = raw_result.get("link", "")
        snippet = raw_result.get("snippet", "")
        
        metadata = {
            "display_link": raw_result.get("displayLink", ""),
            "file_format": raw_result.get("fileFormat", None),
            "mime_type": raw_result.get("mime", None),
            "html_snippet": raw_result.get("htmlSnippet", None),
            "html_title": raw_result.get("htmlTitle", None),
            "image": raw_result.get("pagemap", {}).get("cse_image", [{}])[0].get("src", None) if "pagemap" in raw_result else None,
            "query_text": query.text
        }
        
        # Check if result is an ad (not directly available in CSE API, but we can infer)
        is_ad = False
        
        # Extract proper attribution
        attribution = {
            "source": "Google",
            "source_url": f"https://www.google.com/search?q={urlencode({'q': query.text})}"
        }
        
        # Look for cached version
        cached_url = None
        if "cacheId" in raw_result:
            cached_url = f"https://webcache.googleusercontent.com/search?q=cache:{raw_result['cacheId']}:{url}"
        
        return SearchResult(
            title=title,
            url=url,
            snippet=snippet,
            provider=self.name,
            rank=rank,
            metadata=metadata,
            is_ad=is_ad,
            cached_url=cached_url,
            attribution=attribution
        )

# llama_metasearch/providers/bing.py
"""Bing search provider implementation."""

import os
import json
import logging
import aiohttp
from typing import List, Dict, Any, Optional
from urllib.parse import urlencode

from .base import SearchProvider
from ..models.result import SearchResult
from ..models.query import Query

logger = logging.getLogger(__name__)


class BingSearchProvider(SearchProvider):
    """
    Bing search provider using the Bing Web Search API.
    
    This class implements the SearchProvider interface for Bing Web Search.
    """
    
    BASE_URL = "https://api.bing.microsoft.com/v7.0/search"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the Bing search provider.
        
        Args:
            api_key: Bing API key. If None, will try to load from BING_API_KEY env var.
            **kwargs: Additional parameters to pass to the search API.
        """
        api_key = api_key or os.environ.get("BING_API_KEY")
        
        if not api_key:
            logger.warning("No Bing API key provided. Searches will fail.")
        
        super().__init__(name="Bing", api_key=api_key, **kwargs)
    
    async def search(self, query: Query, num_results: int = 10) -> List[SearchResult]:
        """
        Perform a Bing search with the given query.
        
        Args:
            query: The search query.
            num_results: Maximum number of results to return.
            
        Returns:
            A list of search results.
        """
        if not self.api_key:
            logger.error("Bing search failed: Missing API key")
            return []
        
        self.wait_for_rate_limit()
        
        params = {
            "q": query.processed_text,
            "count": min(num_results, 50)  # Bing API max is 50 per request
        }
        
        # Add optional parameters
        if "mkt" in query.parameters:  # Market code
            params["mkt"] = query.parameters["mkt"]
            
        if "setLang" in query.parameters:  # UI language
            params["setLang"] = query.parameters["setLang"]
            
        if "safeSearch" in query.parameters:  # Safe search
            params["safeSearch"] = query.parameters["safeSearch"]
        
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                results = []
                
                url = f"{self.BASE_URL}?{urlencode(params)}"
                logger.debug(f"Bing search URL: {url}")
                
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        response_text = await response.text()
                        logger.error(f"Bing search failed: {response.status} - {response_text}")
                        return []
                    
                    data = await response.json()
                    
                    if "webPages" not in data or "value" not in data["webPages"]:
                        logger.warning("No results found in Bing response")
                        return []
                    
                    # Process results
                    for i, item in enumerate(data["webPages"]["value"]):
                        result = self.format_result(item, i + 1, query)
                        results.append(result)
                        
                        if len(results) >= num_results:
                            break
                
                return results
        
        except Exception as e:
            logger.exception(f"Error during Bing search: {e}")
            return []
    
    def validate_api_key(self) -> bool:
        """
        Validate the provided Bing API key.
        
        Returns:
            True if the API key is valid, False otherwise.
        """
        return self.api_key is not None
    
    def format_result(self, raw_result: Dict[str, Any], rank: int, query: Query) -> SearchResult:
        """
        Format a raw Bing result into a SearchResult object.
        
        Args:
            raw_result: Raw result from the Bing API.
            rank: Rank of the result.
            query: Original query.
            
        Returns:
            A formatted SearchResult.
        """
        title = raw_result.get("name", "Untitled")
        url = raw_result.get("url", "")
        snippet = raw_result.get("snippet", "")
        
        metadata = {
            "display_url": raw_result.get("displayUrl", ""),
            "date_last_crawled": raw_result.get("dateLastCrawled", None),
            "query_text": query.text
        }
        
        # Check if result is an ad (not directly available in Bing API)
        is_ad = False
        
        # Extract proper attribution
        attribution = {
            "source": "Bing",
            "source_url": f"https://www.bing.com/search?q={urlencode({'q': query.text})}"
        }
        
        # No direct cached URL available from Bing API
        cached_url = None
        
        return SearchResult(
            title=title,
            url=url,
            snippet=snippet,
            provider=self.name,
            rank=rank,
            metadata=metadata,
            is_ad=is_ad,
            cached_url=cached_url,
            attribution=attribution
        )

# llama_metasearch/providers/duckduckgo.py
"""DuckDuckGo search provider implementation."""

import os
import json
import logging
import aiohttp
from typing import List, Dict, Any, Optional
from urllib.parse import urlencode

from .base import SearchProvider
from ..models.result import SearchResult
from ..models.query import Query

logger = logging.getLogger(__name__)


class DuckDuckGoSearchProvider(SearchProvider):
    """
    DuckDuckGo search provider using the DuckDuckGo API.
    
    This class implements the SearchProvider interface for DuckDuckGo.
    Note: DuckDuckGo doesn't have an official API, so this uses a proxy service.
    """
    
    BASE_URL = "https://api.duckduckgo.com/"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the DuckDuckGo search provider.
        
        Args:
            api_key: Not required for DuckDuckGo, but can be used for premium services.
            **kwargs: Additional parameters to pass to the search API.
        """
        super().__init__(name="DuckDuckGo", api_key=api_key, **kwargs)
    
    async def search(self, query: Query, num_results: int = 10) -> List[SearchResult]:
        """
        Perform a DuckDuckGo search with the given query.
        
        Args:
            query: The search query.
            num_results: Maximum number of results to return.
            
        Returns:
            A list of search results.
        """
        self.wait_for_rate_limit()
        
        params = {
            "q": query.processed_text,
            "format": "json",
            "no_html": "1",
            "no_redirect": "1"
        }
        
        # Add optional parameters
        if "region" in query.parameters:
            params["kl"] = query.parameters["region"]
            
        if "safe" in query.parameters:
            params["kp"] = "-2" if query.parameters["safe"] == "off" else "1"
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.BASE_URL}?{urlencode(params)}"
                logger.debug(f"DuckDuckGo search URL: {url}")
                
                async with session.get(url) as response:
                    if response.status != 200:
                        response_text = await response.text()
                        logger.error(f"DuckDuckGo search failed: {response.status} - {response_text}")
                        return []
                    
                    data = await response.json()
                    
                    # Process results
                    results = []
                    
                    # Handle Instant Answer if available
                    if data.get("Abstract") or data.get("AbstractText"):
                        ia_result = {
                            "title": data.get("Heading", "DuckDuckGo Instant Answer"),
                            "url": data.get("AbstractURL", ""),
                            "abstract": data.get("AbstractText", data.get("Abstract", "")),
                            "source": data.get("AbstractSource", ""),
                            "type": "instant_answer"
                        }
                        
                        results.append(self.format_result(ia_result, 0, query))
                    
                    # Handle Related Topics
                    rank = len(results) + 1
                    for topic in data.get("RelatedTopics", []):
                        if "Result" in topic and "Text" in topic:
                            topic_result = {
                                "title": topic.get("Text", "").split(" - ")[0],
                                "url": topic.get("FirstURL", ""),
                                "snippet": topic.get("Text", ""),
                                "icon": topic.get("Icon", {}).get("URL", ""),
                                "type": "related_topic"
                            }
                            
                            results.append(self.format_result(topic_result, rank, query))
                            rank += 1
                            
                            if len(results) >= num_results:
                                break
                                
                    return results[:num_results]
        
        except Exception as e:
            logger.exception(f"Error during DuckDuckGo search: {e}")
            return []
    
    def validate_api_key(self) -> bool:
        """
        Validate the provided API key.
        
        Returns:
            True if the API key is valid, False otherwise.
        """
        # DuckDuckGo doesn't require an API key
        return True
    
    def format_result(self, raw_result: Dict[str, Any], rank: int, query: Query) -> SearchResult:
        """
        Format a raw DuckDuckGo result into a SearchResult object.
        
        Args:
            raw_result: Raw result from the DuckDuckGo API.
            rank: Rank of the result.
            query: Original query.
            
        Returns:
            A formatted SearchResult.
        """
        title = raw_result.get("title", "Untitled")
        url = raw_result.get("url", "")
        snippet = raw_result.get("snippet", raw_result.get("abstract", ""))
        
        metadata = {
            "result_type": raw_result.get("type", "web"),
            "icon": raw_result.get("icon", ""),
            "source": raw_result.get("source", ""),
            "query_text": query.text
        }
        
        # Check if result is an ad (DuckDuckGo doesn't serve ads via API)
        is_ad = False
        
        # Extract proper attribution
        attribution = {
            "source": "DuckDuckGo",
            "source_url": f"https://duckduckgo.com/?q={urlencode({'q': query.text})}"
        }
        
        # No cached URL available from DuckDuckGo
        cached_url = None
        
        return SearchResult(
            title=title,
            url=url,
            snippet=snippet,
            provider=self.name,
            rank=rank,
            metadata=metadata,
            is_ad=is_ad,
            cached_url=cached_url,
            attribution=attribution
        )

# llama_metasearch/providers/__init__.py
"""Search provider module initialization."""

from .base import SearchProvider
from .bing import BingSearchProvider
from .duckduckgo import DuckDuckGoSearchProvider
from .google import GoogleSearchProvider

__all__ = [
    "SearchProvider", 
    "GoogleSearchProvider", 
    "BingSearchProvider", 
    "DuckDuckGoSearchProvider"
]

# llama_metasearch/engine_selector.py
"""Adaptive engine selector for choosing optimal search providers."""

import asyncio
import json
import logging
import os
import pickle
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

from .models.query import Query, QueryIntent
from .providers.base import SearchProvider

logger = logging.getLogger(__name__)


class AdaptiveEngineSelector:
    """
    Adaptive engine selector using reinforcement learning and heuristic fallbacks.
    
    This class is responsible for selecting the most appropriate search engines
    for a given query based on historical performance, query characteristics,
    and potentially a reinforcement learning model.
    """
    
    def __init__(
        self,
        available_providers: Dict[str, SearchProvider],
        model_path: Optional[str] = None,
        use_rl: bool = True,
        min_providers: int = 1,
        max_providers: int = 3,
        exploration_rate: float = 0.1,
        learning_rate: float = 0.01,
        reward_discount: float = 0.9,
        state_features: List[str] = None,
        history_file: Optional[str] = None
    ):
        """
        Initialize the adaptive engine selector.
        
        Args:
            available_providers: Dictionary of available search providers.
            model_path: Path to a pre-trained RL model file. If None, will start with a new model.
            use_rl: Whether to use reinforcement learning for selection.
            min_providers: Minimum number of providers to select.
            max_providers: Maximum number of providers to select.
            exploration_rate: Epsilon for epsilon-greedy exploration.
            learning_rate: Learning rate for model updates.
            reward_discount: Discount factor for future rewards.
            state_features: List of features to use for state representation.
            history_file: Path to a file for storing selection history.
        """
        self.available_providers = available_providers
        self.use_rl = use_rl
        self.min_providers = min_providers
        self.max_providers = max_providers
        self.exploration_rate = exploration_rate
        self.learning_rate = learning_rate
        self.reward_discount = reward_discount
        
        # Default state features if none provided
        self.state_features = state_features or [
            "query_length",
            "intent_type",
            "has_local_intent",
            "time_of_day",
            "is_question"
        ]
        
        # Load or initialize RL model
        self.model: Dict[str, Dict[str, float]] = {}
        if use_rl and model_path and os.path.exists(model_path):
            self._load_model(model_path)
        else:
            self._initialize_model()
        
        # History for tracking selections and outcomes
        self.history: List[Dict[str, Any]] = []
        self.history_file = history_file
        if history_file and os.path.exists(history_file):
            self._load_history()
            
        # Provider performance metrics
        self.provider_metrics: Dict[str, Dict[str, float]] = {
            provider_name: {
                "success_rate": 0.5,  # Start with neutral
                "avg_latency": 1.0,
                "result_quality": 0.5,
                "usage_count": 0
            }
            for provider_name in available_providers
        }
        
        # Intent to provider mapping based on heuristics
        self.intent_provider_map = {
            QueryIntent.INFORMATIONAL: ["Google", "DuckDuckGo", "Bing"],
            QueryIntent.NAVIGATIONAL: ["Google", "Bing"],
            QueryIntent.TRANSACTIONAL: ["Google", "Bing"],
            QueryIntent.COMMERCIAL: ["Google", "Bing"],
            QueryIntent.LOCAL: ["Google", "Bing"],
            QueryIntent.VISUAL: ["Bing", "Google"],
            QueryIntent.NEWS: ["Bing", "Google", "DuckDuckGo"],
            QueryIntent.UNDEFINED: ["Google", "DuckDuckGo", "Bing"]
        }
    
    def _initialize_model(self) -> None:
        """Initialize a new RL model."""
        self.model = {}
        # We'll populate the model as we see states
    
    def _load_model(self, model_path: str) -> None:
        """
        Load a trained model from a file.
        
        Args:
            model_path: Path to the model file.
        """
        try:
            if model_path.endswith('.json'):
                with open(model_path, 'r') as f:
                    self.model = json.load(f)
            elif model_path.endswith('.pkl'):
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
            else:
                raise ValueError(f"Unsupported model file format: {model_path}")
            
            logger.info(f"Loaded RL model from {model_path} with {len(self.model)} states")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self._initialize_model()
    
    def save_model(self, model_path: str) -> None:
        """
        Save the current model to a file.
        
        Args:
            model_path: Path where to save the model.
        """
        try:
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            
            if model_path.endswith('.json'):
                with open(model_path, 'w') as f:
                    json.dump(self.model, f)
            elif model_path.endswith('.pkl'):
                with open(model_path, 'wb') as f:
                    pickle.dump(self.model, f)
            else:
                raise ValueError(f"Unsupported model file format: {model_path}")
            
            logger.info(f"Saved RL model to {model_path}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def _load_history(self) -> None:
        """Load selection history from file."""
        try:
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
            logger.info(f"Loaded selection history from {self.history_file} with {len(self.history)} entries")
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            self.history = []
    
    def save_history(self) -> None:
        """Save selection history to file."""
        if not self.history_file:
            return
            
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f)
            logger.info(f"Saved selection history to {self.history_file}")
        except Exception as e:
            logger.error(f"Error saving history: {e}")
    
    def _extract_state_features(self, query: Query) -> Dict[str, Any]:
        """
        Extract features from a query to represent the state.
        
        Args:
            query: The query to extract features from.
            
        Returns:
            Dictionary of state features.
        """
        state = {}
        
        # Query length (binned)
        query_length = len(query.text)
        if query_length <= 3:
            state["query_length"] = "short"
        elif query_length <= 10:
            state["query_length"] = "medium"
        else:
            state["query_length"] = "long"
        
        # Intent type
        state["intent_type"] = query.intent.value
        
        # Has local intent
        state["has_local_intent"] = query.locality != "global"
        
        # Time of day (if available)
        if "time_of_day" in query.context:
            state["time_of_day"] = query.context["time_of_day"]
        else:
            import datetime
            hour = datetime.datetime.now().hour
            if 5 <= hour < 12:
                state["time_of_day"] = "morning"
            elif 12 <= hour < 17:
                state["time_of_day"] = "afternoon"
            elif 17 <= hour < 22:
                state["time_of_day"] = "evening"
            else:
                state["time_of_day"] = "night"
        
        # Is question
        state["is_question"] = query.text.strip().endswith("?")
        
        # Additional features that might be in context
        for feature in self.state_features:
            if feature in query.context and feature not in state:
                state[feature] = query.context[feature]
        
        return state
    
    def _state_to_key(self, state: Dict[str, Any]) -> str:
        """
        Convert a state dictionary to a string key for the model.
        
        Args:
            state: State dictionary.
            
        Returns:
            String representation of the state.
        """
        # Sort keys for consistent representation
        return "|".join(f"{k}:{v}" for k, v in sorted(state.items()))
    
    def _get_action_value(self, state_key: str, action: Tuple[str, ...]) -> float:
        """
        Get the value of an action in a state.
        
        Args:
            state_key: The state key.
            action: The action (tuple of provider names).
            
        Returns:
            The estimated value of the action.
        """
        action_key = ",".join(sorted(action))
        
        if state_key not in self.model:
            self.model[state_key] = {}
            
        if action_key not in self.model[state_key]:
            # Initialize with a default value
            self.model[state_key][action_key] = 0.5
            
        return self.model[state_key][action_key]
    
    def _update_action_value(self, state_key: str, action: Tuple[str, ...], reward: float) -> None:
        """
        Update the value of an action with a reward.
        
        Args:
            state_key: The state key.
            action: The action (tuple of provider names).
            reward: The reward received.
        """
        action_key = ",".join(sorted(action))
        
        if state_key not in self.model:
            self.model[state_key] = {}
            
        if action_key not in self.model[state_key]:
            self.model[state_key][action_key] = 0.5
            
        # Simple update rule
        old_value = self.model[state_key][action_key]
        self.model[state_key][action_key] += self.learning_rate * (reward - old_value)
    
    def _get_heuristic_providers(self, query: Query) -> List[str]:
        """
        Select providers based on heuristics.
        
        Args:
            query: The search query.
            
        Returns:
            List of provider names.
        """
        # Get providers preferred for this intent
        preferred = self.intent_provider_map.get(query.intent, 
                                                ["Google", "DuckDuckGo", "Bing"])
        
        # Filter to available providers and ensure we have enough
        available_preferred = [p for p in preferred if p in self.available_providers]
        
        if len(available_preferred) < self.min_providers:
            # Add more providers from available
            additional = [p for p in self.available_providers if p not in available_preferred]
            available_preferred.extend(additional[:self.min_providers - len(available_preferred)])
        
        # Limit to max providers
        return available_preferred[:self.max_providers]
    
    def _get_rl_providers(self, state: Dict[str, Any]) -> List[str]:
        """
        Select providers using the RL model.
        
        Args:
            state: The current state.
            
        Returns:
            List of provider names.
        """
        state_key = self._state_to_key(state)
        
        # Generate all possible combinations of providers within min/max limits
        import itertools
        provider_names = list(self.available_providers.keys())
        all_actions = []
        
        for n in range(self.min_providers, self.max_providers + 1):
            for combo in itertools.combinations(provider_names, n):
                all_actions.append(combo)
        
        # Epsilon-greedy selection
        if random.random() < self.exploration_rate:
            # Explore: random action
            selected_action = random.choice(all_actions)
        else:
            # Exploit: best known action
            if state_key not in self.model:
                self.model[state_key] = {}
                
            # Initialize values for actions not seen
            for action in all_actions:
                action_key = ",".join(sorted(action))
                if action_key not in self.model[state_key]:
                    self.model[state_key][action_key] = 0.5
            
            # Select best action
            best_value = -float('inf')
            best_actions = []
            
            for action in all_actions:
                value = self._get_action_value(state_key, action)
                if value > best_value:
                    best_value = value
                    best_actions = [action]
                elif value == best_value:
                    best_actions.append(action)
            
            # Break ties randomly
            selected_action = random.choice(best_actions)
        
        return list(selected_action)
    
    async def select_providers(self, query: Query) -> Dict[str, SearchProvider]:
        """
        Select the appropriate search providers for a query.
        
        Args:
            query: The search query.
            
        Returns:
            Dictionary of selected provider names to provider instances.
        """
        # Extract state features
        state = self._extract_state_features(query)
        state_key = self._state_to_key(state)
        
        # Select providers based on strategy
        if self.use_rl:
            provider_names = self._get_rl_providers(state)
        else:
            provider_names = self._get_heuristic_providers(query)
        
        # Record the selection
        selection_record = {
            "query_id": query.query_id,
            "query_text": query.text,
            "state": state,
            "state_key": state_key,
            "selected_providers": provider_names,
            "timestamp": query.timestamp
        }
        
        self.history.append(selection_record)
        
        # Log selection
        logger.debug(f"Selected providers for query '{query.text}': {provider_names}")
        
        # Return dictionary of provider instances
        return {name: self.available_providers[name] for name in provider_names 
                if name in self.available_providers}
    
    def record_feedback(
        self,
        query_id: str,
        provider_performances: Dict[str, Dict[str, float]],
        overall_reward: float
    ) -> None:
        """
        Record feedback about the performance of selected providers.
        
        Args:
            query_id: ID of the query.
            provider_performances: Dictionary of provider performance metrics.
            overall_reward: Overall reward for the selection.
        """
        # Find the selection record
        selection_record = None
        for record in self.history:
            if record.get("query_id") == query_id:
                selection_record = record
                break
        
        if not selection_record:
            logger.warning(f"No selection record found for query ID {query_id}")
            return
        
        # Update the record with feedback
        selection_record["provider_performances"] = provider_performances
        selection_record["overall_reward"] = overall_reward
        
        # Update provider metrics
        for provider, metrics in provider_performances.items():
            if provider in self.provider_metrics:
                # Update running averages
                self.provider_metrics[provider]["usage_count"] += 1
                count = self.provider_metrics[provider]["usage_count"]
                
                # Update success rate
                if "success_rate" in metrics:
                    old_rate = self.provider_metrics[provider]["success_rate"]
                    self.provider_metrics[provider]["success_rate"] = (
                        old_rate * (count - 1) / count + metrics["success_rate"] / count
                    )
                
                # Update latency
                if "latency" in metrics:
                    old_latency = self.provider_metrics[provider]["avg_latency"]
                    self.provider_metrics[provider]["avg_latency"] = (
                        old_latency * (count - 1) / count + metrics["latency"] / count
                    )
                
                # Update result quality
                if "result_quality" in metrics:
                    old_quality = self.provider_metrics[provider]["result_quality"]
                    self.provider_metrics[provider]["result_quality"] = (
                        old_quality * (count - 1) / count + metrics["result_quality"] / count
                    )
        
        # Update RL model if using RL
        if self.use_rl:
            self._update_action_value(
                selection_record["state_key"],
                tuple(selection_record["selected_providers"]),
                overall_reward
            )
        
        # Save history
        self.save_history()

# llama_metasearch/aggregator.py
"""Federated result aggregator for combining search results."""

import itertools
import logging
import math
from typing import Any, Callable, Dict, List, Optional, Tuple

from .models.result import SearchResult

logger = logging.getLogger(__name__)


class FederatedAggregator:
    """
    Federated search result aggregator with multiple ranking strategies.
    
    This class is responsible for combining search results from multiple
    providers into a single, cohesive ranked list.
    """
    
    def __init__(
        self,
        strategy: str = "rrf",
        rrf_k: int = 60,
        custom_scoring_function: Optional[Callable[[SearchResult], float]] = None,
        bias_correction: bool = True,
        preserve_provider_diversity: bool = True,
        interleaving_depth: int = 3
    ):
        """
        Initialize the federated aggregator.
        
        Args:
            strategy: Aggregation strategy. Options: "rrf" (Reciprocal Rank Fusion),
                "interleaving", "round_robin", "weighted", or "custom".
            rrf_k: Constant for Reciprocal Rank Fusion.
            custom_scoring_function: Custom function for scoring results if strategy is "custom".
            bias_correction: Whether to apply bias correction during aggregation.
            preserve_provider_diversity: Whether to ensure diversity in provider results.
            interleaving_depth: Depth to use for interleaving strategy.
        """
        self.strategy = strategy
        self.rrf_k = rrf_k
        self.custom_scoring_function = custom_scoring_function
        self.bias_correction = bias_correction
        self.preserve_provider_diversity = preserve_provider_diversity
        self.interleaving_depth = interleaving_depth
        
        self.strategy_map = {
            "rrf": self._reciprocal_rank_fusion,
            "interleaving": self._interleaving,
            "round_robin": self._round_robin,
            "weighted": self._weighted_ranking,
            "custom": self._custom_ranking
        }
        
        if strategy not in self.strategy_map:
            logger.warning(f"Unknown strategy '{strategy}', falling back to 'rrf'")
            self.strategy = "rrf"
    
    def aggregate(
        self,
        provider_results: Dict[str, List[SearchResult]],
        provider_weights: Optional[Dict[str, float]] = None,
        max_results: int = 20
    ) -> Tuple[List[SearchResult], Dict[str, Any]]:
        """
        Aggregate search results from multiple providers into a single ranked list.
        
        Args:
            provider_results: Dictionary mapping provider names to their search results.
            provider_weights: Optional weights for each provider for weighted strategies.
            max_results: Maximum number of results to return.
            
        Returns:
            Tuple containing:
                - List of aggregated search results.
                - Dictionary with aggregation statistics.
        """
        # Default weights if not provided
        if provider_weights is None:
            provider_weights = {provider: 1.0 for provider in provider_results}
        
        # Initialize statistics
        stats = {
            "strategy": self.strategy,
            "provider_result_counts": {provider: len(results) 
                                      for provider, results in provider_results.items()},
            "total_input_results": sum(len(results) for results in provider_results.values()),
            "duplicates_removed": 0,
            "bias_corrections_applied": 0
        }
        
        # Apply the selected strategy
        if self.strategy in self.strategy_map:
            strategy_function = self.strategy_map[self.strategy]
            aggregated = strategy_function(provider_results, provider_weights)
        else:
            logger.error(f"Strategy '{self.strategy}' not implemented")
            aggregated = []
        
        # Apply post-processing
        if self.preserve_provider_diversity:
            aggregated = self._ensure_provider_diversity(aggregated)
        
        # Limit to max_results
        final_results = aggregated[:max_results]
        
        # Update statistics
        stats["total_output_results"] = len(final_results)
        stats["provider_diversity"] = len(set(result.provider for result in final_results))
        
        # Provider distribution in final results
        provider_distribution = {}
        for result in final_results:
            provider = result.provider
            if provider not in provider_distribution:
                provider_distribution[provider] = 0
            provider_distribution[provider] += 1
        stats["provider_distribution"] = provider_distribution
        
        return final_results, stats
    
    def _reciprocal_rank_fusion(
        self,
        provider_results: Dict[str, List[SearchResult]],
        provider_weights: Dict[str, float]
    ) -> List[SearchResult]:
        """
        Implement Reciprocal Rank Fusion algorithm.
        
        Args:
            provider_results: Results from each provider.
            provider_weights: Weights for each provider.
            
        Returns:
            Aggregated and ranked results.
        """
        # Calculate RRF scores for each result
        result_scores: Dict[str, Tuple[float, SearchResult]] = {}
        
        for provider, results in provider_results.items():
            provider_weight = provider_weights.get(provider, 1.0)
            
            for rank, result in enumerate(results, 1):
                result_id = result.result_id
                
                # RRF score: weight / (rank + k)
                rrf_score = provider_weight / (rank + self.rrf_k)
                
                if result_id in result_scores:
                    # Add scores for duplicate results
                    current_score, _ = result_scores[result_id]
                    result_scores[result_id] = (current_score + rrf_score, result)
                else:
                    result_scores[result_id] = (rrf_score, result)
        
        # Sort by score (descending)
        sorted_results = [result for _, result in 
                         sorted(result_scores.values(), key=lambda x: x[0], reverse=True)]
        
        return sorted_results
    
    def _interleaving(
        self,
        provider_results: Dict[str, List[SearchResult]],
        provider_weights: Dict[str, float]
    ) -> List[SearchResult]:
        """
        Implement interleaving strategy to mix results from different providers.
        
        Args:
            provider_results: Results from each provider.
            provider_weights: Weights for each provider.
            
        Returns:
            Interleaved results.
        """
        # Sort providers by weight (descending)
        sorted_providers = sorted(provider_weights.keys(), 
                                 key=lambda p: provider_weights.get(p, 0.0),
                                 reverse=True)
        
        # Create iterators for each provider's results
        provider_iterators = {
            provider: iter(results) 
            for provider, results in provider_results.items() 
            if provider in sorted_providers
        }
        
        # Interleave to the specified depth
        interleaved_results = []
        seen_result_ids = set()
        
        for depth in range(self.interleaving_depth):
            for provider in sorted_providers:
                if provider not in provider_iterators:
                    continue
                    
                iterator = provider_iterators[provider]
                
                try:
                    # Get next result from this provider
                    result = next(iterator)
                    
                    # Skip if we've seen this result already
                    if result.result_id in seen_result_ids:
                        continue
                    
                    seen_result_ids.add(result.result_id)
                    interleaved_results.append(result)
                    
                except StopIteration:
                    # No more results from this provider
                    del provider_iterators[provider]
        
        # Add any remaining results in rank order
        for provider in sorted_providers:
            if provider not in provider_iterators:
                continue
                
            remaining_results = list(provider_iterators[provider])
            for result in remaining_results:
                if result.result_id not in seen_result_ids:
                    seen_result_ids.add(result.result_id)
                    interleaved_results.append(result)
        
        return interleaved_results
    
    def _round_robin(
        self,
        provider_results: Dict[str, List[SearchResult]],
        provider_weights: Dict[str, float]
    ) -> List[SearchResult]:
        """
        Implement round-robin strategy to select results in turn from each provider.
        
        Args:
            provider_results: Results from each provider.
            provider_weights: Weights for each provider.
            
        Returns:
            Results selected in round-robin fashion.
        """
        # Sort providers by weight (descending)
        sorted_providers = sorted(provider_weights.keys(), 
                                 key=lambda p: provider_weights.get(p, 0.0),
                                 reverse=True)
        
        round_robin_results = []
        seen_result_ids = set()
        
        # Keep taking one result from each provider until all are exhausted
        max_rounds = max(len(results) for results in provider_results.values())
        
        for round_num in range(max_rounds):
            for provider in sorted_providers:
                results = provider_results[provider]
                
                if round_num < len(results):
                    result = results[round_num]
                    
                    # Skip if we've seen this result already
                    if result.result_id in seen_result_ids:
                        continue
                    
                    seen_result_ids.add(result.result_id)
                    round_robin_results.append(result)
        
        return round_robin_results
    
    def _weighted_ranking(
        self,
        provider_results: Dict[str, List[SearchResult]],
        provider_weights: Dict[str, float]
    ) -> List[SearchResult]:
        """
        Implement weighted ranking based on provider weights and result rank.
        
        Args:
            provider_results: Results from each provider.
            provider_weights: Weights for each provider.
            
        Returns:
            Results ranked by weighted scores.
        """
        # Calculate weighted scores for each result
        result_scores: Dict[str, Tuple[float, SearchResult]] = {}
        
        for provider, results in provider_results.items():
            provider_weight = provider_weights.get(provider, 1.0)
            
            for result in results:
                result_id = result.result_id
                
                # Original rank (lower is better)
                rank = result.rank if result.rank > 0 else len(results)
                
                # Higher ranks get lower scores, so invert
                rank_score = 1.0 / rank
                
                # Apply provider weight
                weighted_score = provider_weight * rank_score
                
                if result_id in result_scores:
                    # Take the higher score for duplicate results
                    current_score, _ = result_scores[result_id]
                    if weighted_score > current_score:
                        result_scores[result_id] = (weighted_score, result)
                else:
                    result_scores[result_id] = (weighted_score, result)
        
        # Sort by score (descending)
        sorted_results = [result for _, result in 
                         sorted(result_scores.values(), key=lambda x: x[0], reverse=True)]
        
        return sorted_results
    
    def _custom_ranking(
        self,
        provider_results: Dict[str, List[SearchResult]],
        provider_weights: Dict[str, float]
    ) -> List[SearchResult]:
        """
        Use a custom scoring function to rank results.
        
        Args:
            provider_results: Results from each provider.
            provider_weights: Weights for each provider.
            
        Returns:
            Results ranked by custom score.
        """
        if not self.custom_scoring_function:
            logger.warning("Custom scoring function not provided, falling back to RRF")
            return self._reciprocal_rank_fusion(provider_results, provider_weights)
        
        # Flatten all results
        all_results = []
        for provider, results in provider_results.items():
            all_results.extend(results)
        
        # Remove duplicates (keeping first occurrence)
        unique_results = {}
        for result in all_results:
            if result.result_id not in unique_results:
                unique_results[result.result_id] = result
        
        # Score each result using the custom function
        scored_results = []
        for result in unique_results.values():
            try:
                score = self.custom_scoring_function(result)
                scored_results.append((score, result))
            except Exception as e:
                logger.error(f"Error in custom scoring function: {e}")
                # Assign a low score
                scored_results.append((0.0, result))
        
        # Sort by score (descending)
        sorted_results = [result for _, result in 
                         sorted(scored_results, key=lambda x: x[0], reverse=True)]
        
        return sorted_results
    
    def _ensure_provider_diversity(self, results: List[SearchResult]) -> List[SearchResult]:
        """
        Ensure diversity in the results by reordering to avoid clusters from the same provider.
        
        Args:
            results: List of search results.
            
        Returns:
            Reordered results with increased provider diversity.
        """
        if not results:
            return []
            
        # Group results by provider
        provider_groups = {}
        for result in results:
            provider = result.provider
            if provider not in provider_groups:
                provider_groups[provider] = []
            provider_groups[provider].append(result)
        
        # Create diversity-aware ordering
        diverse_results = []
        
        # Sort providers by the rank of their best result
        provider_first_ranks = {
            provider: min(r.rank for r in results) 
            for provider, results in provider_groups.items()
        }
        
        sorted_providers = sorted(provider_groups.keys(), 
                                 key=lambda p: provider_first_ranks.get(p, float('inf')))
        
        # Take results in round-robin fashion from each provider
        max_rounds = max(len(group) for group in provider_groups.values())
        
        for round_num in range(max_rounds):
            for provider in sorted_providers:
                group = provider_groups[provider]
                
                if round_num < len(group):
                    diverse_results.append(group[round_num])
        
        return diverse_results

# llama_metasearch/deduplicator.py
"""Cross-engine deduplicator for removing duplicate search results."""

import asyncio
import hashlib
import logging
import re
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.parse import urlparse

try:
    from sentence_transformers import SentenceTransformer, util
    HAVE_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAVE_SENTENCE_TRANSFORMERS = False

from .models.result import SearchResult

logger = logging.getLogger(__name__)


class CrossEngineDeduplicator:
    """
    Cross-engine deduplicator for detecting and removing duplicate search results.
    
    This class uses a combination of URL analysis, text similarity, and other
    metrics to identify duplicate results across different search engines.
    """
    
    def __init__(
        self,
        embedding_model: str = "paraphrase-MiniLM-L6-v2",
        similarity_threshold: float = 0.85,
        url_based: bool = True,
        content_based: bool = True,
        title_based: bool = True,
        normalize_urls: bool = True,
        keep_strategy: str = "higher_rank",
        batch_size: int = 32
    ):
        """
        Initialize the deduplicator.
        
        Args:
            embedding_model: Name of the sentence-transformers model to use for similarity.
            similarity_threshold: Threshold for considering texts as similar (0.0 to 1.0).
            url_based: Whether to use URL-based deduplication.
            content_based: Whether to use content-based deduplication.
            title_based: Whether to use title-based deduplication.
            normalize_urls: Whether to normalize URLs (remove params, fragments, etc).
            keep_strategy: Strategy for keeping one of duplicates ("higher_rank" or "first").
            batch_size: Batch size for processing embeddings.
        """
        self.similarity_threshold = similarity_threshold
        self.url_based = url_based
        self.content_based = content_based
        self.title_based = title_based
        self.normalize_urls = normalize_urls
        self.keep_strategy = keep_strategy
        self.batch_size = batch_size
        
        # Initialize embedding model if available
        self.model = None
        if HAVE_SENTENCE_TRANSFORMERS and (content_based or title_based):
            try:
                self.model = SentenceTransformer(embedding_model)
                logger.info(f"Initialized sentence transformer model: {embedding_model}")
            except Exception as e:
                logger.error(f"Error loading sentence transformer model: {e}")
                logger.warning("Content-based and title-based deduplication will be limited")
    
    def _normalize_url(self, url: str) -> str:
        """
        Normalize a URL by removing query parameters, fragments, etc.
        
        Args:
            url: The URL to normalize.
            
        Returns:
            Normalized URL.
        """
        if not self.normalize_urls:
            return url
            
        parsed = urlparse(url)
        
        # Build normalized URL
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        
        # Optionally keep important query parameters
        if parsed.query:
            # Keep only essential parameters (customize as needed)
            essential_params = ['id', 'article', 'p', 'page']
            query_parts = parsed.query.split('&')
            kept_parts = []
            
            for part in query_parts:
                if '=' in part:
                    param = part.split('=')[0]
                    if param in essential_params:
                        kept_parts.append(part)
            
            if kept_parts:
                normalized += '?' + '&'.join(kept_parts)
        
        return normalized
    
    def _get_content_hash(self, result: SearchResult) -> str:
        """
        Get a hash of the content (snippet) for a result.
        
        Args:
            result: Search result.
            
        Returns:
            Hash of the normalized content.
        """
        # Normalize text: lowercase, remove excess whitespace
        content = result.snippet.lower()
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Hash the content
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_title_hash(self, result: SearchResult) -> str:
        """
        Get a hash of the title for a result.
        
        Args:
            result: Search result.
            
        Returns:
            Hash of the normalized title.
        """
        # Normalize text: lowercase, remove excess whitespace
        title = result.title.lower()
        title = re.sub(r'\s+', ' ', title).strip()
        
        # Hash the title
        return hashlib.md5(title.encode()).hexdigest()
    
    async def _compute_embeddings(self, texts: List[str]) -> List[Any]:
        """
        Compute embeddings for a list of texts.
        
        Args:
            texts: List of texts to encode.
            
        Returns:
            List of embeddings.
        """
        if not self.model:
            logger.warning("Sentence transformer model not available")
            return [None] * len(texts)
        
        # Process in batches to avoid memory issues
        embeddings = []
        
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            try:
                batch_embeddings = self.model.encode(batch, convert_to_tensor=True)
                embeddings.extend(batch_embeddings)
            except Exception as e:
                logger.error(f"Error computing embeddings: {e}")
                # Return placeholder embeddings for this batch
                embeddings.extend([None] * len(batch))
        
        return embeddings
    
    async def deduplicate(
        self,
        results: List[SearchResult]
    ) -> Tuple[List[SearchResult], Dict[str, Any]]:
        """
        Deduplicate search results.
        
        Args:
            results: List of search results to deduplicate.
            
        Returns:
            Tuple containing:
                - Deduplicated list of search results.
                - Dictionary with deduplication statistics.
        """
        if not results:
            return [], {"duplicates_removed": 0}
        
        # Initialize stats
        stats = {
            "total_input": len(results),
            "duplicates_removed": 0,
            "url_duplicates": 0,
            "content_duplicates": 0,
            "title_duplicates": 0,
            "semantic_duplicates": 0
        }
        
        # Track which results to keep
        keep_results = set(range(len(results)))
        duplicate_groups = []
        
        # URL-based deduplication
        if self.url_based:
            url_map = {}
            
            for i, result in enumerate(results):
                normalized_url = self._normalize_url(result.url)
                
                if normalized_url in url_map:
                    # Found duplicate
                    existing_idx = url_map[normalized_url]
                    duplicate_groups.append((existing_idx, i, "url"))
                    stats["url_duplicates"] += 1
                else:
                    url_map[normalized_url] = i
        
        # Content hash-based deduplication
        if self.content_based:
            content_map = {}
            
            for i, result in enumerate(results):
                if i not in keep_results:
                    continue  # Already marked as duplicate
                    
                content_hash = self._get_content_hash(result)
                
                if content_hash in content_map:
                    # Found duplicate
                    existing_idx = content_map[content_hash]
                    duplicate_groups.append((existing_idx, i, "content"))
                    stats["content_duplicates"] += 1
                else:
                    content_map[content_hash] = i
        
        # Title hash-based deduplication
        if self.title_based:
            title_map = {}
            
            for i, result in enumerate(results):
                if i not in keep_results:
                    continue  # Already marked as duplicate
                    
                title_hash = self._get_title_hash(result)
                
                if title_hash in title_map:
                    # Found duplicate
                    existing_idx = title_map[title_hash]
                    duplicate_groups.append((existing_idx, i, "title"))
                    stats["title_duplicates"] += 1
                else:
                    title_map[title_hash] = i
        
        # Semantic similarity-based deduplication
        if (self.content_based or self.title_based) and self.model:
            # Prepare texts for embedding
            title_texts = [result.title for result in results]
            snippet_texts = [result.snippet for result in results]
            
            # Compute embeddings in parallel
            title_embeddings, snippet_embeddings = await asyncio.gather(
                self._compute_embeddings(title_texts),
                self._compute_embeddings(snippet_texts)
            )
            
            # Check for semantic duplicates
            for i in range(len(results)):
                if i not in keep_results:
                    continue  # Already marked as duplicate
                
                for j in range(i + 1, len(results)):
                    if j not in keep_results:
                        continue  # Already marked as duplicate
                    
                    # Check title similarity if available
                    title_sim = 0.0
                    if title_embeddings[i] is not None and title_embeddings[j] is not None:
                        title_sim = util.pytorch_cos_sim(
                            title_embeddings[i], title_embeddings[j]
                        ).item()
                    
                    # Check snippet similarity if available
                    snippet_sim = 0.0
                    if snippet_embeddings[i] is not None and snippet_embeddings[j] is not None:
                        snippet_sim = util.pytorch_cos_sim(
                            snippet_embeddings[i], snippet_embeddings[j]
                        ).item()
                    
                    # Consider as duplicate if either similarity is above threshold
                    if title_sim > self.similarity_threshold or snippet_sim > self.similarity_threshold:
                        duplicate_groups.append((i, j, "semantic"))
                        stats["semantic_duplicates"] += 1
        
        # Resolve all duplicates using the keep strategy
        for original_idx, duplicate_idx, dup_type in duplicate_groups:
            if original_idx not in keep_results or duplicate_idx not in keep_results:
                continue  # Already handled
            
            # Determine which one to keep
            if self.keep_strategy == "higher_rank":
                original_rank = results[original_idx].rank
                duplicate_rank = results[duplicate_idx].rank
                
                if duplicate_rank < original_rank:  # Lower rank is better
                    keep_idx, remove_idx = duplicate_idx, original_idx
                else:
                    keep_idx, remove_idx = original_idx, duplicate_idx
            else:  # "first" strategy
                keep_idx, remove_idx = original_idx, duplicate_idx
            
            # Mark for removal
            if remove_idx in keep_results:
                keep_results.remove(remove_idx)
                stats["duplicates_removed"] += 1
        
        # Build final deduplicated list
        deduplicated = [results[i] for i in sorted(keep_results)]
        
        stats["total_output"] = len(deduplicated)
        
        return deduplicated, stats

# llama_metasearch/intent_classifier.py
"""Query intent classification for optimizing search provider selection."""

import json
import logging
import os
import pickle
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    HAVE_TRANSFORMERS = True
except ImportError:
    HAVE_TRANSFORMERS = False

from .models.query import Query, QueryIntent, QueryLocality

logger = logging.getLogger(__name__)


class QueryIntentClassifier:
    """
    Classifier for determining the intent and characteristics of search queries.
    
    This class uses a combination of heuristics and machine learning models
    to classify the intent of search queries.
    """
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        use_pretrained: bool = True,
        use_heuristics: bool = True,
        heuristics_confidence_threshold: float = 0.8,
        cache_size: int = 1000
    ):
        """
        Initialize the query intent classifier.
        
        Args:
            model_path: Path to a local model or name of a pretrained model.
            use_pretrained: Whether to use a pretrained model.
            use_heuristics: Whether to use heuristic rules for classification.
            heuristics_confidence_threshold: Confidence threshold for heuristic rules.
            cache_size: Size of the classification cache.
        """
        self.use_pretrained = use_pretrained
        self.use_heuristics = use_heuristics
        self.heuristics_confidence_threshold = heuristics_confidence_threshold
        
        # Intent label mapping
        self.intent_labels = {
            0: QueryIntent.INFORMATIONAL,
            1: QueryIntent.NAVIGATIONAL,
            2: QueryIntent.TRANSACTIONAL,
            3: QueryIntent.COMMERCIAL,
            4: QueryIntent.LOCAL,
            5: QueryIntent.VISUAL,
            6: QueryIntent.NEWS,
            7: QueryIntent.UNDEFINED
        }
        
        # Locality label mapping
        self.locality_labels = {
            0: QueryLocality.GLOBAL,
            1: QueryLocality.LOCAL,
            2: QueryLocality.REGIONAL,
            3: QueryLocality.NATIONAL,
            4: QueryLocality.UNDEFINED
        }
        
        # Initialize model
        self.intent_model = None
        self.intent_tokenizer = None
        self.locality_model = None
        self.locality_tokenizer = None
        
        if use_pretrained and HAVE_TRANSFORMERS:
            self._initialize_models(model_path)
        
        # Cache for previously classified queries
        self.cache: Dict[str, Tuple[QueryIntent, float, QueryLocality, float]] = {}
        self.cache_size = cache_size
    
    def _initialize_models(self, model_path: Optional[str] = None) -> None:
        """
        Initialize the classification models.
        
        Args:
            model_path: Path to model files or pretrained model name.
        """
        try:
            # For intent classification
            if model_path and os.path.exists(os.path.join(model_path, "intent_model")):
                # Load local model
                self.intent_tokenizer = AutoTokenizer.from_pretrained(
                    os.path.join(model_path, "intent_tokenizer")
                )
                self.intent_model = AutoModelForSequenceClassification.from_pretrained(
                    os.path.join(model_path, "intent_model")
                )
                logger.info("Loaded local intent classification model")
            else:
                # Use default pretrained model
                model_name = "distilbert-base-uncased-finetuned-sst-2-english"
                self.intent_tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.intent_model = AutoModelForSequenceClassification.from_pretrained(model_name)
                logger.info(f"Loaded pretrained intent model: {model_name}")
            
            # For locality classification
            if model_path and os.path.exists(os.path.join(model_path, "locality_model")):
                # Load local model
                self.locality_tokenizer = AutoTokenizer.from_pretrained(
                    os.path.join(model_path, "locality_tokenizer")
                )
                self.locality_model = AutoModelForSequenceClassification.from_pretrained(
                    os.path.join(model_path, "locality_model")
                )
                logger.info("Loaded local locality classification model")
            else:
                # Use same model for both tasks if no dedicated locality model is available
                self.locality_tokenizer = self.intent_tokenizer
                self.locality_model = self.intent_model
                logger.info("Using intent model for locality classification as well")
            
            # Move models to GPU if available
            if torch.cuda.is_available():
                self.intent_model = self.intent_model.to("cuda")
                self.locality_model = self.locality_model.to("cuda")
                logger.info("Models moved to GPU")
                
        except Exception as e:
            logger.error(f"Error initializing models: {e}")
            self.intent_model = None
            self.intent_tokenizer = None
            self.locality_model = None
            self.locality_tokenizer = None
    
    def _apply_heuristics(self, query_text: str) -> Tuple[Optional[QueryIntent], float, Optional[QueryLocality], float]:
        """
        Apply heuristic rules to classify query intent and locality.
        
        Args:
            query_text: Text of the query.
            
        Returns:
            Tuple containing:
                - Identified intent or None if no clear intent.
                - Confidence score for the intent.
                - Identified locality or None if no clear locality.
                - Confidence score for the locality.
        """
        text = query_text.lower().strip()
        
        # Intent heuristics
        intent = None
        intent_confidence = 0.0
        
        # Navigational intent markers
        if re.search(r'\b(go to|open|visit|website|login|sign in|homepage)\b', text):
            intent = QueryIntent.NAVIGATIONAL
            intent_confidence = 0.9
        # Transactional intent markers
        elif re.search(r'\b(buy|purchase|order|download|book|reserve|subscribe|shop)\b', text):
            intent = QueryIntent.TRANSACTIONAL
            intent_confidence = 0.9
        # Commercial intent markers
        elif re.search(r'\b(price|cost|cheap|expensive|review|compare|vs|versus|deal|best)\b', text):
            intent = QueryIntent.COMMERCIAL
            intent_confidence = 0.85
        # Local intent markers
        elif re.search(r'\b(near me|nearby|local|location|directions|map)\b', text):
            intent = QueryIntent.LOCAL
            intent_confidence = 0.9
        # Visual intent markers
        elif re.search(r'\b(image|picture|photo|wallpaper|diagram|graph|chart|infographic)\b', text):
            intent = QueryIntent.VISUAL
            intent_confidence = 0.9
        # News intent markers
        elif re.search(r'\b(news|latest|update|recent|today|yesterday|this week|breaking)\b', text):
            intent = QueryIntent.NEWS
            intent_confidence = 0.9
        # Informational intent as fallback
        elif re.search(r'\b(how|what|when|where|why|who|which|define|meaning)\b', text) or text.endswith('?'):
            intent = QueryIntent.INFORMATIONAL
            intent_confidence = 0.8
        
        # Locality heuristics
        locality = None
        locality_confidence = 0.0
        
        # Local locality markers
        if re.search(r'\b(near me|nearby|local|within|around here)\b', text):
            locality = QueryLocality.LOCAL
            locality_confidence = 0.9
        # Regional locality markers
        elif re.search(r'\b(in [a-z]+ county|in [a-z]+ region|regional|district)\b', text):
            locality = QueryLocality.REGIONAL
            locality_confidence = 0.85
        # National locality markers
        elif re.search(r'\b(in [a-z]+|country|nationwide|national|domestic)\b', text) and not re.search(r'\b(website|login|forum)\b', text):
            locality = QueryLocality.NATIONAL
            locality_confidence = 0.8
        # Global as fallback for certain topics
        elif re.search(r'\b(world|global|international|universal|everywhere)\b', text):
            locality = QueryLocality.GLOBAL
            locality_confidence = 0.9
        
        return intent, intent_confidence, locality, locality_confidence
    
    def _model_classification(self, query_text: str) -> Tuple[QueryIntent, float, QueryLocality, float]:
        """
        Classify query using ML models.
        
        Args:
            query_text: Text of the query.
            
        Returns:
            Tuple containing:
                - Classified intent.
                - Confidence score for the intent.
                - Classified locality.
                - Confidence score for the locality.
        """
        if not HAVE_TRANSFORMERS or not self.intent_model or not self.intent_tokenizer:
            # No model available, use fallback
            return (
                QueryIntent.INFORMATIONAL, 0.5,
                QueryLocality.GLOBAL, 0.5
            )
        
        try:
            # Intent classification
            inputs = self.intent_tokenizer(
                query_text,
                return_tensors="pt",
                truncation=True,
                max_length=128
            )
            
            if torch.cuda.is_available():
                inputs = {k: v.to("cuda") for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.intent_model(**inputs)
                intent_logits = outputs.logits
                
                # Apply softmax to get probabilities
                intent_probs = torch.nn.functional.softmax(intent_logits, dim=1)[0]
                
                # Get highest probability class
                intent_idx = torch.argmax(intent_probs).item()
                intent_conf = intent_probs[intent_idx].item()
                
                # Map to intent
                if intent_idx < len(self.intent_labels):
                    intent = self.intent_labels[intent_idx]
                else:
                    intent = QueryIntent.UNDEFINED
                    
            # Locality classification (using same approach)
            with torch.no_grad():
                outputs = self.locality_model(**inputs)
                locality_logits = outputs.logits
                
                # Apply softmax to get probabilities
                locality_probs = torch.nn.functional.softmax(locality_logits, dim=1)[0]
                
                # Get highest probability class
                locality_idx = torch.argmax(locality_probs).item()
                locality_conf = locality_probs[locality_idx].item()
                
                # Map to locality
                if locality_idx < len(self.locality_labels):
                    locality = self.locality_labels[locality_idx]
                else:
                    locality = QueryLocality.UNDEFINED
                
            return intent, intent_conf, locality, locality_conf
                
        except Exception as e:
            logger.error(f"Error in model classification: {e}")
            return (
                QueryIntent.UNDEFINED, 0.0,
                QueryLocality.UNDEFINED, 0.0
            )
    
    def _add_to_cache(self, query_text: str, result: Tuple[QueryIntent, float, QueryLocality, float]) -> None:
        """
        Add a classification result to the cache.
        
        Args:
            query_text: Query text.
            result: Classification result.
        """
        # Remove oldest item if cache is full
        if len(self.cache) >= self.cache_size:
            # Simple LRU: remove first item
            self.cache.pop(next(iter(self.cache)))
        
        self.cache[query_text] = result
    
    def classify(self, query: Query) -> Query:
        """
        Classify the intent and locality of a query.
        
        Args:
            query: The query to classify.
            
        Returns:
            The query with intent and locality updated.
        """
        # Check if already classified with high confidence
        if query.intent != QueryIntent.UNDEFINED and query.locality != QueryLocality.UNDEFINED:
            return query
            
        query_text = query.text.lower().strip()
        
        # Check cache first
        if query_text in self.cache:
            intent, intent_conf, locality, locality_conf = self.cache[query_text]
            query.intent = intent
            query.locality = locality
            return query
        
        # Apply heuristics if enabled
        if self.use_heuristics:
            h_intent, h_intent_conf, h_locality, h_locality_conf = self._apply_heuristics(query_text)
            
            # Use heuristic results if confidence is high enough
            has_intent = h_intent is not None and h_intent_conf >= self.heuristics_confidence_threshold
            has_locality = h_locality is not None and h_locality_conf >= self.heuristics_confidence_threshold
            
            if has_intent and has_locality:
                # Both determined with high confidence
                self._add_to_cache(query_text, (h_intent, h_intent_conf, h_locality, h_locality_conf))
                query.intent = h_intent
                query.locality = h_locality
                return query
        else:
            h_intent, h_intent_conf = None, 0.0
            h_locality, h_locality_conf = None, 0.0
            has_intent, has_locality = False, False
        
        # Use model classification if available and needed
        if self.use_pretrained and (not has_intent or not has_locality):
            m_intent, m_intent_conf, m_locality, m_locality_conf = self._model_classification(query_text)
            
            # Determine final intent (prefer heuristics if confidence is high)
            if has_intent:
                intent, intent_conf = h_intent, h_intent_conf
            else:
                intent, intent_conf = m_intent, m_intent_conf
                
            # Determine final locality (prefer heuristics if confidence is high)
            if has_locality:
                locality, locality_conf = h_locality, h_locality_conf
            else:
                locality, locality_conf = m_locality, m_locality_conf
        else:
            # If no model and heuristics didn't give high confidence
            if has_intent:
                intent, intent_conf = h_intent, h_intent_conf
            else:
                intent, intent_conf = QueryIntent.INFORMATIONAL, 0.5
                
            if has_locality:
                locality, locality_conf = h_locality, h_locality_conf
            else:
                locality, locality_conf = QueryLocality.GLOBAL, 0.5
        
        # Add to cache and update query
        self._add_to_cache(query_text, (intent, intent_conf, locality, locality_conf))
        query.intent = intent
        query.locality = locality
        
        return query
    
    def save_cache(self, cache_path: str) -> None:
        """
        Save the classification cache to a file.
        
        Args:
            cache_path: Path where to save the cache.
        """
        try:
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            with open(cache_path, 'wb') as f:
                pickle.dump(self.cache, f)
            logger.info(f"Saved classification cache to {cache_path}")
        except Exception as e:
            logger.error(f"Error saving cache: {e}")
    
    def load_cache(self, cache_path: str) -> None:
        """
        Load the classification cache from a file.
        
        Args:
            cache_path: Path to the cache file.
        
                            result =