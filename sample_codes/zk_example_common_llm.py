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
