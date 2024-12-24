from setuptools import setup, find_packages
setup(
	name='torch-former',
	version='0.0.1-alpha',
	packages=find_packages(),
	author='Sane Punk',
	author_email = "punk00pp@gmail.com",
	url = "https://lazy-punk.github.io/",
	license = "MIT",
	install_requires=[
		'numpy',
		'matplotlib',
		'seaborn',
		'scikit-learn',
	],
	classifiers=[
		'Development Status :: 3 - Alpha',  # Adjust development status as needed
		'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Topic :: Scientific/Engineering :: Artificial Intelligence'],
	description="""
	torch-former is a Python package offering a suite of plotting functions to visualize machine learning models and data. It provides intuitive and customizable plots to aid in model evaluation and data analysis.
	
	**Key Features:**
	
	- **Model Evaluation Plots:** Visualize confusion matrices, ROC curves, and precision-recall curves.
	- **Data Visualization:** Generate heatmaps, pair plots, and feature importance plots.
	- **Compatibility:** Seamlessly integrates with popular machine learning libraries like scikit-learn and TensorFlow.
	
	**Ideal for:**
	
	- Data scientists and machine learning practitioners seeking efficient visualization tools.
	- Educators aiming to demonstrate model performance and data relationships.
	- Researchers requiring clear and customizable plots for publications.
	
	Enhance your machine learning workflow with torch-former' comprehensive plotting capabilities.
	"""
)

