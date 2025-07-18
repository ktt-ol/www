+++
title = "Tiny WS2812 Controller"
date = "2016-12-09T00:00:00"
authors = ["sre"]

[taxonomies]
Typ = ["Projekt"]
Serie = ["Hardware"]

[extra]
thumbnail = "/media/blog/2016/tiny-ws2812-controller/thumbnail.jpg"
repository = "https://github.com/ktt-ol/access-control-system/tree/master/tiny-led-firmware"
+++

For our access control system we ~~needed~~ wanted a few
multi-colored status LEDs. Nowadays that basically means, that one gets a few
ws2812b LEDs, since they are quite cheap and already provide a serial
interface. Unfortunately most microcontrollers including the Raspberry Pi have
no hardware accelerated interface for their protocol. For our access control
system we thus use an ATtiny85 to translate from the ws2812 protocol to a more
common serial protocol: I²C.

Below you can see how the ATtiny85 is supposed to be wired. Basically it needs
power supply, the I²C interface (SDA, SCL) and the input pin of the first ws2812b
LED must be connected to the pin labeled WS2812b. There is also a mode pin, that
should be connected to some GPIO of the system controlling the ATtiny85. More on
that later.

![Hardware Connection](/media/blog/2016/tiny-ws2812-controller/attiny-connections.svg)

The ATtiny85 firmware consists of 3 parts: A driver for the ws2812b LEDs, a driver
for the I²C interface and some glue-code. Let's have a look at each part.

## WS2812b driver

Like most microcontrollers, the ATtiny does not have hardware support for the
ws2812 protocol. That means we need to generate it ourself by bit-banging one
of its I/O pins. Since we did not connect any crystal to our ATtiny to keep the
circuit simple, we use it with the internally generated 8MHz clock signal. So
one instruction is supposed to be roughly 125ns. By studying the ws2812b timing
diagram below, you can see, that we must be able to switch the pin at least
within 350ns. As you can see the timing may be possible, but while we are
updating the LEDs it's impossible to do anything else.

![WS2812b timings](/media/blog/2016/tiny-ws2812-controller/ws2812b-timings.svg)

The driver itself solves the timing issues by disabling interrupts, since any
ever so short interruption will break the ws2812b timing. Then it loops over
a supplied array of LED values. There it loops over the bits of each byte and
based upon its value it either starts with a long high-sequence or a short
high-sequence followed by the matching low-sequence. All of that is done in
inline assembly to avoid the compiler doing optimizations breaking the timing.

In theory it would be possible to handle interrupts during the ws2812 update,
if we used a timer instead of counting instructions for the precise timing. But
our interrupt service routine would have to be finished within 1 or 2
instructions, since we must satisfy the 350ns timing. Obviously that's not helping
much.

## I²C driver

Fortunately the ATtiny85 does have hardware support for the I²C protocol making
things a bit easier on this side. The hardware block capable of I²C (master and
slave) support inside of the ATtiny85 is named Universal Serial Interface AKA
<b>USI</b>. I²C is a bus-protocol, which usually has one master and multiple
slave devices connected via two wires (not counting ground) named SDA and SCL.

The communication is always started from the master using a start-condition and
stopped by a matching stop-condition. After being initialized the USI module
will generate a interrupt, if it sees a start or stop condition on the bus, so
that it can be handled by our I²C driver.

Then there is a second interrupt for all other i2c related events. Let's ignore
most of them here and just have a look how the data is exchanged. We basically
get an event "data received" for each received byte and "data requested" for
each byte, that should be send. The byte, that should be sent is simple written
to a register of the USI block. Similarly reading the byte when the data received
interrupts comes in, we get the byte written to the bus. All bit-level stuff is
handled by the hardware.

Our I²C driver also takes care of checking the address (while it receives the
data destined for other devices it will ignore any ongoing communication, that
was not started with its own address as recipient) and implementing an eeprom
style interface.

The base idea of our eeprom style interface is, that we receive
colour-information from the I2C master by receiving a single byte for the LED
number and 4 bytes with colour data. From a bus-level point of view this is
exactly the same as an eeprom with 8-bit address size and 32-bit value size.
For example if you want to set the 11th LED to white you would send the following via
I²C: `<device-addr> 0x0a 0xff 0xff 0xff 0x00`. There will be more information
about the additional byte in a later section of this documentation. Once the
I²C driver received all 4 bytes it will call i2c_recv(led, data) in the glue
code.

## Glue code

The glue-code combines the I²C driver with the ws2812b driver to something
useful.  For this task it stores all information received from the I²C driver
into an array for the LEDs. Similarly it has a second array, which contains the
LED colour information for the ws2812b driver. In theory the same array could be
used for both implementations, but the split-architecture allows us to implement
some fancy features in our glue-code. Unfortunately it also means, that we need
quite a bit of memory (4 bytes for i2c data + 3 bytes for ws2812b data = 7 byte).
With the ATtiny85 only having 512 byte of memory that means we can talk to a max.
of about 60-70 LEDs.

Now let's have a look at the 4th byte sent via the I²C interface. Appart from
directly setting a LED color, our ATtiny85 should also be able to blink LEDs
and fade to some other color. This is encoded in the fourth byte. It's upper
two bits (7&8) can be used to let the ATtiny85 know, what we want to do with
the LED:

* 00 = set color directly
* 01 = fade to color
* 10 = blink (on/off in specified color)
* 11 = glow (slowly decrease brightness by 25% and then increase again)

The remaining 6 bit are a time value, which is multiplied by 31.25ms (32Hz
base). For fade mode it describes how long it the (linear) fading should take.
For blink and glow mode it describes how long a half period (dark → bright /
bright → dark) should take. This means the max. encodable timing is 2 seconds.

## Mode pin

As described in the ws2812b section, the update requires disabled interrupts.
Updating 50 LEDs requires roughly 62.5us. Disabling the interrupts for such a
long time results in problems with the I²C bus. Thus the USI module must be
disabled while we update the LEDs (or interrupts must be enabled resulting in
broken LED update if there is I²C traffic and thus random blinking).

We worked around the issue by introducing another pin to choose between I²C
mode and LED update mode. In I²C mode (mode pin = high) the LEDs are not
updated and the timer engine for the fading is stopped (important to make the
LEDs blink synchronously). In LED mode (mode pin = low) on the other hand the
I²C interface is disabled.

## Example

Once the firmware is flashed and the hardware wiring is done you can now
control your LEDs using the following interface:

```txt
device_addr = 0x23;
mode_blink = 0x2 &lt;&lt; 6;
gpio_set(mode_pin, 1); // send ATtiny85 into i2c mode
usleep(1000); // wait until ATtiny85 reached i2c mode
i2c_send(device_addr, 0x00, 0x80, 0x00, 0x00, 0x00); // LED0 = red
i2c_send(device_addr, 0x01, 0x00, 0x80, 0x00, 0x00); // LED1 = green
i2c_send(device_addr, 0x02, 0x00, 0x00, 0x80, 0x00); // LED2 = blue
i2c_send(device_addr, 0x03, 0x30, 0x00, 0x20, mode_blink | 8); // LED3 = blink purple @ 2Hz
io_set(mode_pin, 0); // send ATtiny85 into led mode
```
