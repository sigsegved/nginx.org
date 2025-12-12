# ngx_http_image_filter_module模块

**Translator:** Cen Zheng  
**Revision:** 1  
**Language:** cn

`ngx_http_image_filter_module` 模块（0.7.54+）是一个 过滤器，它可以对JPEG,GIF和PNG等图像进行变换。

这个模块并不是默认编译的，需要通过 `--with-http_image_filter_module` 编译选项来启用。

> **Note:** 这个模块使用了 [libgd](http://libgd.org) 库。
推荐使用这个库可用的最新版本；在写这个文档时它的最新版本是2.0.35。

# 配置例子 {#example}

```
location /img/ {
    proxy_pass   http://backend;
    image_filter resize 150 100;
    image_filter rotate 90;
    error_page   415 = /empty;
}

location = /empty {
    empty_gif;
}
```

# 指令 {#directives}

## image_filter

```
Syntax:  image_filter crop width height;
Default: 
Context: location
```

设置图像变换的操作：

**`off`**  
  在所在location关闭模块处理。

**`test`**  
  确保应答是JPEG，GIF或PNG格式的图像。否则错误 415 Unsupported Media Type 将被返回。

**`size`**  
  以JSON格式返回图像信息。例如：

```
{ "img" : { "width": 100, "height": 100, "type": "gif" } }
```

  如果有错误发生，将会返回如下：

```
{}
```

**`rotate` `90` | `180` | `270`**  
  将图像逆时针旋转指定角度。
参数的值可以包含变量。
可以单独使用，或与 `resize` 和 `crop` 变换同时使用.

**`resize` `width` `height`**  
  按比例缩小图像至指定大小。
如果想只指定其中一维，另一维可以指定为：
“ `-` ”。
如果有错误发生，服务器会返回 415 Unsupported Media Type .
参数的值可以包含变量。
当与 `rotate` 参数同时使用时,
旋转发生在缩放 *之后* 。

**`crop` `width` `height`**  
  按比例以图像的最短边为准对图像大小进行缩小，然后裁剪另一边多出来的部分。
如果想只指定其中一维，另一维可以指定为：
“ `-` ”。
如果有错误发生，服务器会返回 415 Unsupported Media Type .
参数的值可以包含变量。
当与 `rotate` 参数同时使用时,
旋转发生在裁剪 *之前* 。

## image_filter_buffer

```
Syntax:  image_filter_buffer size;
Default: 1M
Context: location, http, server
```

设置用来读图像的缓冲区的最大值。 若图像超过这个大小，服务器会返回 415 Unsupported Media Type .

## image_filter_jpeg_quality

```
Syntax:  image_filter_jpeg_quality quality;
Default: 75
Context: location, http, server
```

设置变换后的JPEG图像的 `质量` 。 可配置值： 1 ~ 100 。 更小的值意味着更差的图像质量以及更少需要传输的数据。 推荐的最大值是95. 参数的值可以包含变量。

## image_filter_sharpen

```
Syntax:  image_filter_sharpen percent;
Default: 0
Context: location, http, server
```

增加最终图像的锐度。 锐度百分比可以超过100. 0为关闭锐化。 参数的值可以包含变量。

## image_filter_transparency

```
Syntax:  image_filter_transparency on|off;
Default: on
Context: location, http, server
```

定义当对PNG，或者GIF图像进行颜色变换时是否需要保留透明度。 损失透明度有可能可以获得更高的图像质量。 PNG图像中的alpha通道的透明度默认会一直被保留。

