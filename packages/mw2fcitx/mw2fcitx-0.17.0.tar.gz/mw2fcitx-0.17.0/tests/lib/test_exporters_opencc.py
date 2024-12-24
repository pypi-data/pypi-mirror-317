from mw2fcitx.exporters.opencc import export


def test_opencc_exporter():
    assert (
        export(["测试"]) == "测试\tce'shi\t0\n"
    )

    assert (
        export([
            "测试",
            "琴吹䌷"  # outloudvi/mw2fcitx#16
        ]) == "测试\tce'shi\t0\n"
        "琴吹䌷\tqin'chui'chou\t0\n"
    )

    assert (
        export([
            "测试",
            "无效:词条"
        ]) == "测试\tce'shi\t0\n"
    )

def test_opencc_instinct_pinyin(): # outloudvi/mw2fcitx#29
    assert (
        export([
            "唔呣",
            "嗯啊啊"
        ]) == "唔呣\twu'mu\t0\n"
        "嗯啊啊\ten'a'a\t0\n"
    )

    assert (
        export([
            "唔呣",
            "嗯啊啊"
        ], disable_instinct_pinyin = True
        ) == "唔呣\twu'm\t0\n"
        "嗯啊啊\tn'a'a\t0\n"
    )
