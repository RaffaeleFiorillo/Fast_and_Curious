############################################################################################################################################################

Ficheiros python envolvidos diretamente no jogo: (6 modulos - 2800 linhas de codigo)

_____________________________________________________________________________________________________________________________________________________________
 - main -> modulo principal. Executado, ele da inicio ao jogo:
	# 47 linhas de codigo; 
	# 1 classe; 
	# 0 funções;
_____________________________________________________________________________________________________________________________________________________________	
 - link_functions -> modulo que contem as funçoes que o main chama para a respetiva funçao no jogo (interfaces, menus, partidas, ...):
	# 259 linhas de codigo; 
	# 0 classes; 
	# 21 funções;
_____________________________________________________________________________________________________________________________________________________________
 - menu_classes -> modulo que contém todas as classes responsaveis por criar e gerir menus:
	# 1122 linhas de codigo; 
	# 15 classes; 
	# 0 funções;
_____________________________________________________________________________________________________________________________________________________________
 - entity_classes -> modulo com as classes das entidades/objetos mostradas no jogo (automovel, obstaculos, parts,...):
	# 362 linhas de codigo; 
	# 8 classes; 
	# 0 funções;
_____________________________________________________________________________________________________________________________________________________________
 - game_classes -> modulo com as classes que criam e gerem a parte jogavel do jogo (partidas como "Mission: AI" e "Mission: Parts"):
	# 532 linhas de codigo; 
	# 2 classes; 
	# 0 funções;
_____________________________________________________________________________________________________________________________________________________________
 - functions -> modulo com funções úteis e que são utilizadas por todos os modulos do jogo falados anteriormente:
	# 478 linhas de codigo;
	# 0 classes; 
	# 45 funções;

############################################################################################################################################################
############################################################################################################################################################
O ficheiro python "genetic_algorithm" é o modulo que foi responsavel pela inteligencia artificial do jogo. Não é usado diretamente no jogo,
porque só tinha a função de criar e treinar a neural network usada pelo automóvel. Se for executado vai criar uma nova população de modelos de neural network
e atravez de um algoritmo genético, vai treinar a neural network até o automovel esquivar dos obstaculos sem problema. (228 linhas de codigo)

ATENÇÃO: este e todos os outros modulos, para funcionar, devem estar todos no mesmo diretorio onde tem as pastas com as imagens, sons,... (ou seja no mesmo diretorio do executavel)