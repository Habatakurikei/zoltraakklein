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
