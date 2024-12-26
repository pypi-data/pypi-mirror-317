from setuptools import setup

setup(
    name='provival',
    version='0.0.1',    
    description='Provival',
    url='https://github.com/davidchen0420',
    author='David Chen',
    author_email='davidc.chen@mail.utoronto.ca',
    license='BSD 2-clause',
    packages=['provival'],
    install_requires=['decoupler>=1.8.0',
                      'pandas>=2.2.3',   
                      'scipy>=1.14.1'],
    include_package_data=True,
package_data={"provival": ["data/SC_DB_Human.pickle", "data/SC_DB_Mouse.pickle", "data/SC_DB_Metadata.pickle"]},
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
    ],
)