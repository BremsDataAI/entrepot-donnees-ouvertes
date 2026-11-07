from modele_projet import main


def test_main_affiche_un_message(capsys):
    main()
    assert "Bonjour" in capsys.readouterr().out
