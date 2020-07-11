import re
from collections import namedtuple
from setuptools import setup
from urllib.parse import urlsplit

GitRequirement = namedtuple('GitRequirement', 'url, name')


def read_requirements():
    with open('requirements.txt') as fd:
        requirements = fd.read().splitlines()
    pypi_requirements = []
    git_requirements = {}
    for requirement in requirements:
        requirement = requirement.strip()
        if requirement.startswith('#'):
            continue
        if requirement.startswith('git+'):
            match = re.fullmatch(r'git\+(?P<url>[^#]*)(#egg=(?P<name>.*))?', requirement)
            if not match:
                raise ValueError(f'unable to parse requirement: {requirement}')
            match_dict = match.groupdict()
            if 'name' in match_dict:
                name = urlsplit(match.group('url')).path.split('/')[-1]
                if name.endswith('.git'):
                    name = name[:-4]
                match_dict['name'] = name
            git_requirements[match_dict['name']] = GitRequirement(**match_dict)
        else:
            pypi_requirements.append(requirement)
    return pypi_requirements, git_requirements


def main():
    pypi_requirements, git_requirements = read_requirements()
    setup(
        name='pdfocr',
        version='',
        description='Convert PDF to text via PyTesseract',
        license='MIT',
        author='Justin Li',
        author_email='justinnhli@gmail.com',
        url='https://github.com/justinnhli/pdfocr',
        packages=['pdfocr'],
        scripts=['bin/pdfocr'],
        install_requires=[
            *pypi_requirements,
            *(
                f'{requirement.name} @ git+{requirement.url}'
                for requirement in git_requirements.values()
            ),
        ],
        dependency_links=[
            *(
                f'{requirement.url}#egg={requirement.name}'
                for requirement in git_requirements.values()
            ),
        ],
    )


if __name__ == '__main__':
    main()
