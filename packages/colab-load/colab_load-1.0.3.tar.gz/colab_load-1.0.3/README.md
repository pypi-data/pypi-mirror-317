# Colab Load #

## What is this? ##
Library to download .ipynb from google colab

## Quick Guide ##
	pip install colab-load
One url:

    from colab_load.load import ColabLoad
    import asyncio
    
    colab_load = ColabLoad()
    
    async def main():
        res = await colab_load.load_file_single("https://colab.research.google.com/drive/1QD1TM2TroOEqqtTURpk5sVOmGLQeREv_?usp=sharing",
                                          "file_colab_load", "test_colab_load")
    
        print(res)
    
    asyncio.run(main())



