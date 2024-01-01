const SwordEngine = require("../../SwordEngineCore");
class $ClassName$ extends SwordEngine.GameApplication {
    Start() {
        const GameWindow = new SwordEngine.GameWindow("$GameName$");
        GameWindow.Size = new SwordEngine.DataStruct.Rect(1280, 720);
        GameWindow.Update();
    };
};
module.exports = { $ClassName$ };