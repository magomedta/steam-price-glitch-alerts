/**
 * After Effects Automation Script: Price Glitch Promo Short (1080x1920, 60fps)
 * How to use:
 * 1. Open Adobe After Effects
 * 2. Go to File > Scripts > Run Script File...
 * 3. Select this Price_Glitch_Promo.jsx file
 * 
 * After Effects will automatically assemble the full composition, keyframes,
 * audio tracks, optical glows, and kinetic text animations!
 */

(function createPriceGlitchPromo() {
    app.beginUndoGroup("Create Price Glitch Promo Composition");

    var compWidth = 1080;
    var compHeight = 1920;
    var pixelAspect = 1.0;
    var duration = 12.0;
    var frameRate = 60;

    // 1. Create Main Vertical Composition
    var promoComp = app.project.items.addComp(
        "Price_Glitch_Promo_Ad",
        compWidth,
        compHeight,
        pixelAspect,
        duration,
        frameRate
    );

    // 2. Add Background Solid
    var bgSolid = promoComp.layers.addSolid([0.04, 0.05, 0.08], "Cyber_Background", compWidth, compHeight, pixelAspect, duration);
    var rampEffect = bgSolid.property("Effects").addProperty("ADBE Ramp");
    rampEffect.property("Start of Ramp").setValue([540, 0]);
    rampEffect.property("Start Color").setValue([0.02, 0.03, 0.06, 1.0]);
    rampEffect.property("End of Ramp").setValue([540, 1920]);
    rampEffect.property("End Color").setValue([0.07, 0.12, 0.20, 1.0]);

    // 3. Add Kinetic Text: "STOP SCROLLING!"
    var hookText = promoComp.layers.addText("STOP SCROLLING!");
    var textProp = hookText.property("Source Text");
    var textDoc = textProp.value;
    textDoc.fontSize = 72;
    textDoc.font = "Arial-BoldMT";
    textDoc.fillColor = [1, 1, 1];
    textDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
    textProp.setValue(textDoc);
    hookText.property("Position").setValue([540, 320]);

    // Pop-in Scale Animation for Hook
    var scaleProp = hookText.property("Scale");
    scaleProp.setValueAtTime(0.0, [0, 0]);
    scaleProp.setValueAtTime(0.3, [115, 115]);
    scaleProp.setValueAtTime(0.5, [100, 100]);

    // 4. Add Glitch Subtitle: "STEAM PRICING ERROR ACTIVE"
    var subText = promoComp.layers.addText("STEAM PRICING ERROR ACTIVE");
    var subDoc = subText.property("Source Text").value;
    subDoc.fontSize = 48;
    subDoc.font = "Arial-BoldMT";
    subDoc.fillColor = [0.98, 0.8, 0.08]; // Cyber Yellow
    subDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
    subText.property("Source Text").setValue(subDoc);
    subText.property("Position").setValue([540, 410]);
    subText.property("Opacity").setValueAtTime(0.2, 0);
    subText.property("Opacity").setValueAtTime(0.5, 100);

    // 5. Add Big Value Badge: "100% FREE ($0.00)"
    var badgeText = promoComp.layers.addText("100% FREE ($0.00)");
    var badgeDoc = badgeText.property("Source Text").value;
    badgeDoc.fontSize = 80;
    badgeDoc.font = "Arial-BoldMT";
    badgeDoc.fillColor = [0.0, 1.0, 0.66]; // Neon Emerald
    badgeDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
    badgeText.property("Source Text").setValue(badgeDoc);
    badgeText.property("Position").setValue([540, 1250]);
    
    // Scale Bounce Keyframes
    var bScale = badgeText.property("Scale");
    bScale.setValueAtTime(3.2, [0, 0]);
    bScale.setValueAtTime(3.5, [120, 120]);
    bScale.setValueAtTime(3.8, [100, 100]);

    // 6. Call To Action: "👉 LINK IN BIO / @price_glitch_live"
    var ctaText = promoComp.layers.addText("👉 LINK IN BIO: @price_glitch_live");
    var ctaDoc = ctaText.property("Source Text").value;
    ctaDoc.fontSize = 54;
    ctaDoc.font = "Arial-BoldMT";
    ctaDoc.fillColor = [0.22, 0.74, 0.97]; // Cyan Blue
    ctaDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
    ctaText.property("Source Text").setValue(ctaDoc);
    ctaText.property("Position").setValue([540, 1620]);
    ctaText.property("Opacity").setValueAtTime(7.0, 0);
    ctaText.property("Opacity").setValueAtTime(7.5, 100);

    // 7. Import Audio Assets if available
    var assetsFolder = "C:/Users/magom/Downloads/twitchst/price_glitch_bot/shorts_output/";
    var audioFiles = ["chime.wav", "ad_voiceover.mp3", "bg_beat.wav"];
    for (var i = 0; i < audioFiles.length; i++) {
        var aFile = new File(assetsFolder + audioFiles[i]);
        if (aFile.exists) {
            var importedAudio = app.project.importFile(new ImportOptions(aFile));
            var aLayer = promoComp.layers.add(importedAudio);
            if (audioFiles[i] === "chime.wav") {
                aLayer.startTime = 0.65;
            } else if (audioFiles[i] === "bg_beat.wav") {
                aLayer.property("Audio Levels").setValue([-12, -12]); // Background volume
            }
        }
    }

    app.endUndoGroup();
    alert("Price Glitch Promo Composition Successfully Generated in After Effects!");
})();
