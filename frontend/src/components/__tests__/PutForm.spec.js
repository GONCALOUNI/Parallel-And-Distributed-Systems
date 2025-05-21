import { mount } from '@vue/test-utils'
import PutForm from '../PutForm.vue'

describe('PutForm.vue', () => {
  it('emits submit with key & value', async () => {
    const wrapper = mount(PutForm)
    const inputs = wrapper.findAll('input')
    await inputs[0].setValue('foo')
    await inputs[1].setValue('bar')
    await wrapper.find('button').trigger('submit')
    const ev = wrapper.emitted('submit')[0][0]
    expect(ev).toEqual({ key: 'foo', value: 'bar' })
  })
})