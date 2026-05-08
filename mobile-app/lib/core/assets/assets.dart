import 'package:flutter/rendering.dart';

part 'src/icon_strings.dart';
part 'src/image_strings.dart';
part 'src/logo_strings.dart';
part 'src/svg_strings.dart';

class Assets {
  static ImageStrings images = ImageStrings.instance;
  static IconStrings icons = IconStrings.instance;
  static LogoStrings logos = LogoStrings.instance;
  static SvgStrings svgs = SvgStrings.instance;
}

extension AssetsExtension on String {
  AssetImage get asImageProvider => AssetImage(this);
}
