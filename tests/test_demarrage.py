from entrepot_donnees_ouvertes import main


def test_main_affiche_un_message(capsys):
    main()
    assert "Bonjour" in capsys.readouterr().out
