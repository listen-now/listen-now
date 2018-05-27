test_platform = [
                 "Neteasymusic", 
                 "Xiamimusic", 
                 "QQmusic",
                ]
t = {
	"platform":"x",
	"page":1
	}

for i in test_platform:
	t["platform"] = i
	print(t)
