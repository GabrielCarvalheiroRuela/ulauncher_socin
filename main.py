import subprocess
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction


class SocinExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryListener())
        self.subscribe(ItemEnterEvent, ItemEnterListener())


class KeywordQueryListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ""
        args = query.strip().split()

        if not args or args[0] == "":
            # Sugestões ao digitar apenas "socin"
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/socin.png',
                    name="desliga [minutos]",
                    description="Agenda o desligamento do computador após alguns minutos",
                    on_enter=ExtensionCustomAction({"comando": "desliga"}, keep_app_open=True)
                ),
                ExtensionResultItem(
                    icon='images/socin.png',
                    name="reinicia [minutos]",
                    description="Agenda a reinicialização do computador após alguns minutos",
                    on_enter=ExtensionCustomAction({"comando": "reinicia"}, keep_app_open=True)
                ),
                ExtensionResultItem(
                    icon='images/socin.png',
                    name="cancela",
                    description="Cancela qualquer desligamento ou reinicialização agendada",
                    on_enter=ExtensionCustomAction({"comando": "cancela"}, keep_app_open=False)
                )
            ])

        comando = args[0].lower()

        if comando in ['desliga', 'reinicia']:
            if len(args) != 2 or not args[1].isdigit():
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon='images/socin.png',
                        name=f"{comando} [minutos]",
                        description="Informe o tempo em minutos. Ex: socin desliga 5",
                        on_enter=HideWindowAction()
                    )
                ])

            minutos = int(args[1])

            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/socin.png',
                    name=f"{'Desligar' if comando == 'desliga' else 'Reiniciar'} em {minutos} minuto(s)",
                    description=f"O sistema será {'desligado' if comando == 'desliga' else 'reiniciado'} em {minutos} minuto(s).",
                    on_enter=ExtensionCustomAction({
                        "comando": comando,
                        "minutos": minutos
                    }, keep_app_open=False)
                )
            ])

        elif comando == 'cancela':
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/socin.png',
                    name="Cancelar agendamento",
                    description="Cancela qualquer desligamento ou reinicialização pendente",
                    on_enter=ExtensionCustomAction({
                        "comando": "cancela"
                    }, keep_app_open=False)
                )
            ])

        else:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/socin.png',
                    name="Comando inválido",
                    description="Comandos: desliga, reinicia, cancela",
                    on_enter=HideWindowAction()
                )
            ])


class ItemEnterListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        comando = data.get("comando")
        minutos = data.get("minutos")

        try:
            if comando == 'desliga':

                subprocess.run(["shutdown", "-h", f"+{minutos}"])
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon='images/socin.png',
                        name="Desligamento agendado",
                        description=f"O sistema será desligado em {minutos} minuto(s).",
                        on_enter=HideWindowAction()
                    )
                ])
            elif comando == 'reinicia':
                
                subprocess.run(["shutdown", "-r", f"+{minutos}"])
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon='images/socin.png',
                        name="Reinício agendado",
                        description=f"O sistema será reiniciado em {minutos} minuto(s).",
                        on_enter=HideWindowAction()
                    )
                ])
            elif comando == 'cancela':
                subprocess.run(["shutdown", "-c"])
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon='images/socin.png',
                        name="Agendamento cancelado",
                        description="Nenhum desligamento ou reinício pendente.",
                        on_enter=HideWindowAction()
                    )
                ])
        except Exception as e:
            print(f"Erro ao executar comando: {e}")
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/socin.png',
                    name="Erro ao executar comando",
                    description=str(e),
                    on_enter=HideWindowAction()
                )
            ])


if __name__ == '__main__':
    SocinExtension().run()
