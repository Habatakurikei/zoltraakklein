![Zoltraak Klein Logo](https://repository-images.githubusercontent.com/828559799/cf060405-3975-49a2-987b-6d22ee7528cc)

[![Downloads](https://static.pepy.tech/badge/zoltraakklein)](https://pepy.tech/project/zoltraakklein)
[![Downloads](https://static.pepy.tech/badge/zoltraakklein/month)](https://pepy.tech/project/zoltraakklein)
[![Downloads](https://static.pepy.tech/badge/zoltraakklein/week)](https://pepy.tech/project/zoltraakklein)

# Zoltraak Klein

Zoltraak is a production framework for digital contents like program codes, images, speeches, presentations, books and videos, by working with Large Language Models (LLMs) and generative AIs.

Link to the original project: [Zoltraak](https://github.com/dai-motoki/zoltraak)

This project was pioneered by Daisuke Motoki [@dai-motoki](https://github.com/dai-motoki/). The original system was a command line tool and was sophisticated for generating SaaS project with codes.

Zoltraak Klein ("Small Zoltraak"), ZK in short, is a compact version of the Zoltraak system, designed as a python class to demonstrate the core functionalities of Zoltraak in a more accessible format.

You might notice that Zoltraak derives from a popular spell in Japanese anime/manga "Frieren: Beyond Journey's End".

## Features

- Project naming and initialization
- Generation of "Requirement Document" or "Requests Definition" (RD in short)
- Directory and file generation (explain details later)
- Support for multiple AI models thanks to [LLMMaster](https://github.com/Habatakurikei/llmmaster)
- Various types of digital contents generation

## Supported Contents to Generate

![zk-compiler-list-20240817-EN](https://github.com/user-attachments/assets/3a11d4a4-28b6-4bc4-90f5-3e972021fc3b)

Zoltraak first generates a RD, then starts to generate contents based on the RD. This process is called "Domain Expansion".

The following contents are supported to generate:

- Business Documents (including mermaid diagrams):
  - General business proposal
  - Business plan
  - Consulting proposal
  - Marketing research
  - Business negotiation supporting document
- Multimedia contents:
  - Web articles (with eye-catching image)
  - Presentation slides with Marp (with cover image)
  - Virtual character (with icon, voice and 3D model)
  - Technical book in Epub/PDF format (with cover image and speech audio)
  - Business book in Epub/PDF format, vertically written for Japanese (with cover image and speech audio)
  - Picture book in Epub/PDF format, suitable for children (with images and speech audio)
- Life Style:
  - Cooking recipes (with image)
  - Travel plans (with schedule and image)
  - Outfit recommendations (with image)
- System Development:
  - Project requirements document (with mermaid diagram)
  - Minimum Viable Product consultation document (with mermaid diagram)
  - Project of software or program codes

Note that multimedia contents are not generated in one time but step by step. It may take over 5 minutes to generate all contents.

## Requirements

- Python 3.9 or later
- The following external content generation tools, including npm (Node.js), are necessary:
  - [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli)
  - [Marp CLI](https://github.com/marp-team/marp-cli)
  - [Voicevox](https://voicevox.hiroshiba.jp/)

Confirmed the latest version of Zoltraak Klein works with the following versions:

- Python 3.12.4
- Node.js v20.15.0
- npm 10.7.0
- marp-cli v3.4.0
- mermaid-cli (mmdc) v10.9.1
- Voicevox 0.15.4 (as core version)

## Installation

Install Zoltraak Klein using pip:

```
pip install zoltraakklein
```

## API Key settings

Set up your API keys as environment variables. Minimum requirement is OpenAI API key as default LLM for RD generation.

If you want all the supported data formats of domain expansion, you will need correspondent API keys. In case of missing API keys, an error causes while generating.

The following list shows the acceptable API keys:

- [OpenAI](https://platform.openai.com/)
- [Anthropic](https://console.anthropic.com/)
- [Google](https://ai.google.dev/)
- [Perplexity](https://docs.perplexity.ai/)
- [Groq](https://console.groq.com/keys)
- [Stable Diffusion](https://platform.stability.ai/)
- [Meshy](https://docs.meshy.ai/)
- [Elevenlabs](https://elevenlabs.io/api)
- [Pika.art (third-party API)](https://www.pikapikapika.io/)

For Mac/Linux,

```
export ANTHROPIC_API_KEY="your_anthropic_key"
export GOOGLE_API_KEY="your_google_key"
export GROQ_API_KEY="your_groq_key"
export OPENAI_API_KEY="your_openai_key"
export PERPLEXITY_API_KEY="your_perplexity_key"
export STABLE_DIFFUSION_API_KEY="your_stable_diffusion_key"
export MESHY_API_KEY="your_meshy_key"
export ELEVENLABS_API_KEY="your_elevenlabs_key"
export PIKAPIKAPIKA_API_KEY="your_pikapikapika_key"
```

For Windows (cmd),

```
SET ANTHROPIC_API_KEY=your_anthropic_key
SET GOOGLE_API_KEY=your_google_key
SET GROQ_API_KEY=your_groq_key
SET OPENAI_API_KEY=your_openai_key
SET PERPLEXITY_API_KEY=your_perplexity_key
SET STABLE_DIFFUSION_API_KEY=your_stable_diffusion_key
SET MESHY_API_KEY=your_meshy_key
SET ELEVENLABS_API_KEY=your_elevenlabs_key
SET PIKAPIKAPIKA_API_KEY=your_pikapikapika_key
```

For Windows (PowerShell)

```
$env:ANTHROPIC_API_KEY="your_anthropic_key"
$env:GOOGLE_API_KEY="your_google_key"
$env:GROQ_API_KEY="your_groq_key"
$env:OPENAI_API_KEY="your_openai_key"
$env:PERPLEXITY_API_KEY="your_perplexity_key"
$env:STABLE_DIFFUSION_API_KEY="your_stable_diffusion_key"
$env:MESHY_API_KEY="your_meshy_key"
$env:ELEVENLABS_API_KEY="your_elevenlabs_key"
$env:PIKAPIKAPIKA_API_KEY="your_pikapikapika_key"
```

## Usage

Zoltraak Klein has only 3 steps:

1. Create a new project with name from your request
2. Generate RD from your request
3. Expand the domain for your project, meaning generating contents and directories

Note that multiple times of expansion is required for some content types. You might need to call expand_domain() multiple times. Explain details later.

Once a new project is created, you are not able to go back to the previous step. If you want to change the request, you need to create another project from scratch.

See folder [sample_codes](sample_codes) for downloadable files. Arranged `zk_sample.py` suitable for demonstration.

### Minimal usage of Zoltraak Klein

```python
from zoltraakklein import ZoltraakKlein

# Make an instance of ZoltraakKlein
zk = ZoltraakKlein(
    request="Cloud-based AI-driven accounting system",
    compiler="project_rd",
    verbose=True
)

# Cast Zoltraak (run all the steps, including one time of domain expansion)
zk.cast_zoltraak()
```

In Zoltraak, prompt is often called request (`request`). Keep in mind that OpenAI API key is set before creating this instance.

Zoltraak prepares compiler (`compiler`) to expand content of your request instead of long prompts. Any long sentences, so called prompts, are not welcome.

Compiler is a template to generate RD, necessary items to be filled out are already written in it. By merging your request with an appropriate `compiler`, Zoltraak generates a better RD.

One of the important conceptual points is that digital contents can be generated with a short message by users. This means users can easily generate contents with short request like a spell. This is why Zoltraak is occasionally called "The magical creation framework" in Japan.

You may need to update your mindset of how we shall work with generative AIs in a more relaxed way.

The last initial argument is `verbose`. If True, the process is displayed on the console. Default is False.

With `cast_zoltraak()`, the instance executes project naming, RD generation and a single time of domain expansion. For most of cases, especially business documents, one time of expansion is enough to generate documents and supporting charts.

After execution, a new directory (`project`) is created in the current working directory. And your project folder is generated under `project` folder. The directory name is the project name assigned in Step 1. All the generated contents are stored in that project folder.

### Individual steps

Possible to call individual steps:

```python
import time
from zoltraakklein import ZoltraakKlein
from zoltraakklein.yaml_manager import YAMLManager


zk = ZoltraakKlein(
    request="Short-hair Japanese bartender girl in 20s, anime-style",
    compiler="virtual_human",
    verbose=True
)

# Step 1: Name the requirement
zk.name_for_requirement()

# Step 2: Generate the requirement
zk.generate_requirement()

# Step 3: Expand the domain
while zk.is_expansion_capable():
    try:
        zk.expand_domain()
        while zk.expansion_in_progress:
            time.sleep(1)
    except Exception as e:
        print(e)
        break

# Show the result
if zk.project_menu.exists():
    menu = YAMLManager(str(zk.project_menu))
    print('Menu (list of generated items) is ready.')
    print(zk.project_menu.read_text(encoding="utf-8"))
    print(f'Total {menu.sum_of_items()} files generated.')

print(f'Elapsed time for each step (sec):')
for step, elapsed_time in zk.takt_time.items():
    print(f"    {step}: {elapsed_time}")
print(f'Total elapsed time (sec) = {sum(zk.takt_time.values())}')
```

Each domain expansion takes time, better to set a timer for status check as shown in Step 3. Especially for picture books, it may take around 10 minutes until full contents generation.

### Advanced usage

Zoltraak Klein accepts different LLMs for project naming and RD generation separately.

Below is an example to set a different LLM from the default. ZK will work with the given LLM for both project naming and RD generation.

```python
from zoltraakklein import ZoltraakKlein

request = "Luxury Watches"
compiler = "marketing_research"

llm = {'google': {'provider': 'google',
                  'model': 'gemini-1.5-flash',
                  'max_tokens': 10000,
                  'temperature': 0.3}}

zk = ZoltraakKlein(request=request,
                   compiler=compiler,
                   verbose=True,
                   **llm)
zk.cast_zoltraak()
```

Another example below uses different LLMs for naming and RD generation separately.

```python
from zoltraakklein import ZoltraakKlein

request = "A new sports apparel brand for young men and women"

compiler = "business_plan"

zk = ZoltraakKlein(request=request,
                   compiler=compiler,
                   verbose=True)

llm_naming = {'naming': {'provider': 'anthropic',
                         'model': 'claude-3-haiku-20240307'}}
zk.name_for_requirement(**llm_naming)

llm_req = {'openai': {'provider': 'openai',
                      'model': 'gpt-4o'},
           'anthropic': {'provider': 'anthropic',
                         'model': 'claude-3-haiku-20240307'},
           'google': {'provider': 'google',
                      'model': 'gemini-1.5-flash'}}
zk.generate_requirement(**llm_req)

zk.expand_domain()
```

This case will generate 3 RDs for each LLM under `project` folder. Each key name in `llm_req` is used for part of RD file name to avoid conflict.

Although you can select LLM for project naming and RD generation, any content generation during domain expansion will be done by dedicated LLM and generative AI defined by the system.

## Terminology

There are still hidden terms to understand Zoltraak better.

- Request: short sentence or keywords of what you want instead of long prompt
- Compiler: template to expand your request so that Zoltraak generates better RD
- RD: "Required Document" or "Requirements Definition"
- Domain Expansion: process of generating directories and files based on RD
- Menu: list of generated contents, recording file location, in YAML format
- Architect: an individual python script to generate digital contents
- Instruction: a document that states steps and processes of domain expansion for each compiler, in YAML format as a pair of compiler
- Library (Magic Library): conceptual term of folders containing templates, architects and instructions
- [LLMMaster](https://github.com/Habatakurikei/llmmaster): a python library that consolidates various LLMs and generative AIs for digital content generation

**Important**: compiler and instruction must always be a pair. For proper content generation, name of `compiler` and `instruction` must be coinsident. For example, there are `book_picture.md` in compilers folder and `book_picture.yaml` in instructions folder.

## Compiler List

Set one of the following compilers as `compiler` argument to generate RD.

- Business Documents:
  - `general_proposal`: Generates diverse proposals for businesses, events, projects, education, research, arts, culture, non-profit activities, and policy planning.
  - `business_plan`: Creates comprehensive business plans at the company or organizational level, including materials for investors.
  - `strategic_consultant`: Produces business consulting materials, including assignments, evaluation methods, class diagrams, revenue models, plans, and Fermi estimates.
  - `marketing_research`: Provides market analysis, including size, growth rate, trends, potential customers, needs, competitive research, and stakeholder information.
  - `business_negotiation`: Prepares materials for successful business negotiations, covering customer understanding, competition analysis, proposal evaluation, contract terms, schedules, and budgets.
- Multimedia contents:
  - `web_article`: Creates online content such as blogs, commentaries, and news articles, with suggestions for titles, illustrations, headline structure, and engaging points.
  - `virtual_character`: Develops detailed character profiles for VTubers, AI models, novel characters, and avatars, including personal details, appearance, personality, and abilities.
  - `presentation_marp`: Generates presentation materials as a requirements specification document, producing slides in various formats (marp, PDF, PPTX, PNG) and presentation videos with audio.
  - `book_business`: Creates vertically written business books, including outline, target audience, table of contents, and multiple format outputs (EPUB, PDF, audiobook).
  - `book_technical`: Produces horizontally written technical books on specific scientific or technological topics, with outline, target audience, table of contents, and multiple format outputs.
  - `book_picture`: Designs children's picture books with full hiragana text, illustrations on each page, and multiple format outputs, including read-aloud video.
- Life Style:
  - `cooking_recipe`: Develops comprehensive cooking recipes, including concept, taste, appearance, ingredients, cooking methods, utensils, budget, and storage tips.
  - `travel_plan`: Creates detailed domestic and international travel itineraries, covering destinations, transportation, accommodations, budget, attractions, local cuisine, and cultural tips.
  - `outfit_idea`: Suggests complete outfit concepts, including clothing, hairstyles, makeup, accessories, and items to bring for specific situations.
- System Development:
  - `project_rd`: Generates system development requirements specifications, including related diagrams such as system configuration, business flow, and data flow charts.
  - `software_development`: Produces requirements specifications for software or websites, with the ability to generate multiple source code files and directory structures.
  - `akira_papa`: Provides consultation and development approach suggestions based on the Minimum Viable Product (MVP) concept for those unsure how to proceed with their product ideas.

## Required API keys for each content type during domain expansion

While you can choose LLMs for project naming and RD generation, you need to set up API keys for LLMs used during domain expansion.

The following list shows the required API keys for each content type during domain expansion.

- Business Documents: API not required but Mermaid CLI is required for chart generation.
- Multimedia contents:
  - `web_article`: OpenAI API key for Dall-E image generation.
  - `virtual_character`: OpenAI (image), Voicevox (voice), and Meshy (3D model)
  - `presentation_marp`: OpenAI (image), Voicevox (voice), marp CLI (presentation), and PikaPikaPika (video)
  - `book_business`: OpenAI (image), Voicevox (voice), marp CLI (presentation), and PikaPikaPika (video)
  - `book_technical`: OpenAI (image), Voicevox (voice), marp CLI (presentation), and PikaPikaPika (video)
  - `book_picture`: OpenAI (character icons), Stable Diffusion (page images), Voicevox (voice), marp CLI (presentation), Meshy (3D model), and PikaPikaPika (video)
- Life Style:
  - `cooking_recipe`: OpenAI API key for Dall-E image generation.
  - `travel_plan`: OpenAI API key for Dall-E image generation. And Mermaid CLI is required for timetable generation.
  - `outfit_idea`: OpenAI API key for Dall-E image generation.
- System Development: API not required but Mermaid CLI is required for chart generation.

These are defined by the system. If you want to change them, you need to modify the corresponding pair of architect python code and instruction. See also Terminology.

## Project Structure

- zoltraakklein
  - `__init__.py`: library initialization
  - `config.py`: Settings and constants (reserved words) for the project
  - `utils.py`: Utility functions for file operations and AI interactions
  - `yaml_manager.py`: YAML file management class, which is used for menu and instruction management
  - `zoltraakklein.py`: Main class implementing ZoltraakKlein functionality
  - `architect`: folder of python codes to work as architect (content generation)
  - `compilers`: folder of templates to generate RD for each content type
  - `instructions`: folder of instruction YAML files for each content type
  - `prompts`: folder of "prompt" templates sending to LLMs and generative AIs
  - `rosetta`: folder of supporting text files for translation
  - `templates`: folder of code templates for marp slides and other content types
- `tests`: folder of test codes for pytest
- `pytest.ini`: settings for pytest
- `README.md`: this file
- `README_JA.md`: Japanese version of this description but not up-to-date information
- `setup.py`: setup file for PyPI packaging

## Advanced Usage

### Scalability

Zoltraak Klein itself is a framework.

You can expand functionality (digital contents production) by adding your own architects and instructions.

**Important**: never change or delete files in folders of architect, compilers, instructions, so called "Library". This may cause a serious error.

### Start domain expansion from certain point

Zoltraak Klein does not allow going back the process, but allow resuming domain expansion at a certain point.

If necessary, call member function `load_project()` after ZK instance initialization with a correct compiler (instruction). Indicate your project name in project folder and resuming point of step number existing in the instruction.

Restarting content generation is possible if the previous expansion is successful but failed at current point. The developer does not recommend using this function because `load_project` was arranged for debug purpose.

### Mermaid chart generation in case of Posix systems

**Important**: added in v1.0.4, 2024-08-28

Mermaid CLI requires external browser to generate chart images. If missing to specify browser path when calling `mmdc` command, an error will occur.

This error is not shown in case of Windows because Mermaid CLI uses Microsoft Edge by default. However, in case of Posix systems (Linux, MacOS), `puppeteer-config.json` might be required to add option in command line.

You will need to find path to browser in your system and add to `"executablePath": "path/to/browser"`, see [puppeteer-config.json](zoltraakklein/templates/puppeteer-config.json).

You will also need to modify architect `mermaid_chart.py` to call `mmdc` command with `--puppeteerConfigFile` option. See [mermaid_chart.py](zoltraakklein/architect/mermaid_chart.py) for detail.

Sorry for the inconvenience.

## License

Following the original Zoltraak project, this project is also licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

Thanks to all contributors and users of the Zoltraak project, especially Daisuke Motoki.
