# Unreal Engine cinematic standards

DOCS STATUS: `C:/Users/dinot/OneDrive/Pictures/Documents/Deepsoch/enginex_ideas/.claude/unreal_engien docs/` exists but is EMPTY (checked 2026-10-31). No offline Unreal reference is available yet. Until it is populated, do not assume API/feature details: say the guide is missing, ask the user to add it (or fetch the official page for the one feature needed), and cache the confirmed answer below.

The folder name is misspelled (`engien`); keep that path until the user renames it.

## Use Unreal only when it beats Blender
Large environments, real-time lighting/GI, Niagara-scale VFX, long Sequencer shots, Movie Render Queue output. Don't use it for a scene Blender already renders well on the pods.

## Areas to document once available (priority order)
Sequencer cinematics; Materials; Niagara VFX; Lighting; Animation; Camera systems; Movie Render Queue; Environment creation; Post-processing.

## Check before use
Is an EngineX Unreal operation present in `find_operation` / `list_operations`? If not, Unreal work is blocked: report it, don't fake it.

## Cached confirmed notes
(none yet; append after each verified lookup)
